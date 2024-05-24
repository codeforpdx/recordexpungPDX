from dataclasses import dataclass
from os import path
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Dict, Tuple, Union, Callable, Optional
from zipfile import ZipFile
from collections import UserDict

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject, PdfName, PdfString

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaViolation
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record_summary import RecordSummary
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF
from expungeservice.util import DateWithFuture

DA_ADDRESSES = {
    "baker": "Baker County Courthouse - 1995 Third Street, Suite 320 - Baker City, OR 97814",
    "benton": "District Attorney's Office - 120 NW 4th St. - Corvallis, OR 97330",
    "clackamas": "807 Main Street - Oregon City, OR 97045",
    "clatsop": "Clatsop County District Attorney’s Office - PO Box 149 - Astoria, OR 97103",
    "columbia": "230 Strand St. - Columbia County Courthouse Annex - St. Helens, OR 97051",
    "coos": "Coos County District Attorney's Office - 250 N. Baxter - Coquille, Oregon 97423",
    "crook": "District Attorney - 300 NE 3rd St, Rm. 34 - Prineville, OR 97754",
    "curry": "District Attorney - 94235 Moore Street, #232 - Gold Beach, OR 97444",
    "deschutes": "District Attorney - 1164 NW Bond St. - Bend, OR 97703",
    "douglas": "District Attorney - 1036 SE Douglas Avenue - Justice Building, Room 204 - Roseburg, OR 97470",
    "gilliam": "District Attorney - 221 S. Oregon St - PO Box 636 - Condon, OR 97823",
    "grant": "District Attorney - 201 South Humbolt Street - Canyon City, Oregon, 97820",
    "harney": "District Attorney - 450 N Buena Vista Ave - Burns, OR 97720",
    "hood_river": "District Attorney - 309 State Street  - Hood River, OR 97031",
    "jackson": "District Attorney - 815 W. 10th Street - Medford, Oregon 97501",
    "jefferson": "District Attorney - 129 SW E Street, Suite 102 - Madras, Oregon 97741",
    "josephine": "District Attorney - 500 NW 6th St #16 - Grants Pass, OR 97526",
    "klamath": "District Attorney - 305 Main Street - Klamath Falls, OR 97601",
    "lake": "District Attorney - 513 Center St, Lakeview, OR 97630",
    "lane": "District Attorney - 125 E 8th Ave - Eugene, OR 97401",
    "lincoln": "District Attorney - 225 W Olive St # 100 - Newport, OR 97365",
    "linn": "District Attorney - PO Box 100 - Albany, Oregon 97321",
    "malheur": "District Attorney - 251 B St. West #6 - Vale, OR 97918",
    "marion": "District Attorney - PO Box 14500 - Salem, OR 97309",
    "morrow": "District Attorney - P.O. Box 664 - Heppner, OR  97836",
    "multnomah": "Multnomah County Central Courthouse - 1200 S.W. 1st Avenue, Suite 5200 - Portland, Oregon 97204",
    "polk": "District Attorney - 850 Main Street - Dallas, OR 97338",
    "sherman": "District Attorney - P.O. Box 393 - Moro, OR 97039",
    "tillamook": "District Attorney - 201 Laurel Ave - Tillamook, OR 97141",
    "umatilla": "District Attorney - 216 SE 4th St, Pendleton, OR 97801",
    "union": "District Attorney - 1104 K Ave - La Grande, OR 97850",
    "wallowa": "District Attorney - 101 S. River Street, Rm. 201 - Enterprise, OR 97828",
    "wasco": "District Attorney - 511 Washington St #304 - The Dalles, OR 97058",
    "washington": "District Attorney - 150 N First Avenue, Suite 300 - Hillsboro, OR 97124-3002",
    "wheeler": "District Attorney - P.O. Box 512 - Fossil, OR 97830",
    "yamhill": "District Attorney - 535 NE 5th St #117 - McMinnville, OR 97128",
}


def join_dates_or_strings(arr: List[Union[DateWithFuture, str]], connector: str, date_format: str) -> str:
    def date_to_str(elem):
        return elem.strftime(date_format) if isinstance(elem, DateWithFuture) else elem

    return connector.join(date_to_str(elem) for elem in arr if elem)


class Charges:
    def __init__(self, charges: List[Charge]):
        self._charges = charges

    @property
    def names(self) -> List[str]:
        return [charge.name.title() for charge in self._charges]

    def dates(self, is_disposition=False, unique=True) -> List[DateWithFuture]:
        """
        Collects the dates of the charges.

        :param bool is_disposition: Whether to use the charge.displosition.date.
            If false, the charge.date wil be returned.
        """
        dates = [charge.disposition.date if is_disposition else charge.date for charge in self._charges]

        if unique:
            return list(dict.fromkeys(dates))
        else:
            return list(dates)

    def dispositions(self) -> List[str]:
        return [charge.disposition.status for charge in self._charges]

    @property
    def empty(self) -> bool:
        return len(self._charges) == 0

    def has_any(self, class_or_level) -> bool:
        """
        Check whether there are any charges with a certain attribute.

        :param Any type: Can be the following:
            * string: a charge_type.severity_level, ex. "Felony Class C"
            * class: a charge_type class, ex. FelonyClassC
            * list: a list of strings and/or classes
        """
        if isinstance(class_or_level, str):
            return any([charge.charge_type.severity_level == class_or_level for charge in self._charges])
        elif isinstance(class_or_level, list):
            return any([self.has_any(a_type) for a_type in class_or_level])
        else:
            return any([isinstance(charge.charge_type, class_or_level) for charge in self._charges])

    def has_any_with_getter(self, getter: Callable) -> bool:
        """
        Check whether there are any charges with a certain attribute.

        :param function getter: A function that will be passed a charge instance. It's return
            value will be used in the `any` check.
        """
        return any([getter(charge) for charge in self._charges])


@dataclass
class UserInfo:
    full_name: str
    date_of_birth: str
    mailing_address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    counties_with_cases_to_expunge: List[str]
    has_eligible_convictions: bool


@dataclass
class CaseResults(UserInfo):
    case: Case
    sid: str
    county: str
    case_name: str
    case_number: str
    has_no_balance: bool
    da_number: str
    arresting_agency: Optional[str] = None

    @classmethod
    def build(cls, case: Case, user_info_dict: Dict[str, str], sid: str):
        return cls(
            case=case,
            sid=sid,
            county=case.summary.location,
            case_number=case.summary.case_number,
            case_name=case.summary.name,
            has_no_balance=case.summary.balance_due_in_cents == 0,
            da_number=case.summary.district_attorney_number,
            counties_with_cases_to_expunge=[],
            has_eligible_convictions=False,
            **user_info_dict,
        )

    def __post_init__(self):
        filtered_charges = tuple(c for c in self.case.charges if c.edit_status != EditStatus.DELETE)
        eligible_charges, ineligible_charges = Case.partition_by_eligibility(filtered_charges)
        dismissed, convictions = Case.categorize_charges(eligible_charges)

        self.charges = Charges(list(filtered_charges))
        self.eligible_charges = Charges(eligible_charges)
        self.ineligible_charges = Charges(ineligible_charges)
        self.dismissed = Charges(dismissed)
        self.convictions = Charges(convictions)

    @property
    def da_address(self):
        county = self.county.replace(" ", "_").lower()
        return DA_ADDRESSES.get(county, "")

    @property
    def case_number_with_comments(self):
        with_comments = self.case_number

        if self.has_ineligible_charges:
            in_part = ", ".join(self.short_eligible_ids)
            with_comments = f"{self.case_number} (charge {in_part} only)"

        return with_comments

    ##### All charges #####

    @property
    def charges_all(self) -> List[str]:
        return self.charges.names

    @property
    def arrest_dates(self) -> List[DateWithFuture]:
        """
        Duplicates are removed. Date at position i does not necessary correspond
        to charge at position i.
        """
        return self.charges.dates()

    ##### Eligible charges #####

    @property
    def eligible_charge_names(self) -> List[str]:
        return self.eligible_charges.names

    @property
    def eligible_charges_list(self) -> List[Charge]:
        return list(self.eligible_charges._charges)

    @property
    def eligible_arrest_dates_all(self) -> List[DateWithFuture]:
        """
        Duplicates are kept. Date at position i corresponds to charge i.
        """
        return self.eligible_charges.dates(unique=False)

    @property
    def eligible_dispositions(self) -> List[str]:
        return self.eligible_charges.dispositions()

    @property
    def short_eligible_ids(self) -> List[str]:
        return [charge.ambiguous_charge_id.split("-")[-1] for charge in self.eligible_charges._charges]

    @property
    def has_contempt_of_court(self) -> bool:
        return self.eligible_charges.has_any(ContemptOfCourt)

    @property
    def has_eligible_charges(self) -> bool:
        return not self.eligible_charges.empty

    @property
    def get_has_eligible_convictions(self) -> bool:
        return any([charge for charge in self.eligible_charges._charges if charge.convicted])

    @property
    def has_future_eligible_charges(self) -> bool:
        return (
            len(
                [
                    c
                    for c in self.ineligible_charges._charges
                    if c.expungement_result.charge_eligibility and c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
                ]
            )
            > 0
        )

    @property
    def is_expungeable_now(self) -> bool:
        return self.has_eligible_charges and self.has_no_balance and not self.has_future_eligible_charges

    ##### Ineligible charges #####

    @property
    def has_ineligible_charges(self) -> bool:
        return not self.ineligible_charges.empty

    ##### Dismissed charges #####

    @property
    def dismissed_charges(self) -> List[str]:
        return self.dismissed.names

    @property
    def dismissed_arrest_dates(self) -> List[DateWithFuture]:
        return self.dismissed.dates()

    @property
    def dismissed_dates(self) -> List[DateWithFuture]:
        return self.dismissed.dates(is_disposition=True)

    @property
    def has_no_complaint(self) -> bool:
        return self.dismissed.has_any_with_getter(lambda charge: charge.no_complaint())

    @property
    def has_dismissed(self) -> bool:
        return not self.dismissed.empty

    ##### Convicted charges #####

    @property
    def conviction_charges(self) -> List[str]:
        return self.convictions.names

    @property
    def conviction_dates(self) -> List[DateWithFuture]:
        return self.convictions.dates(is_disposition=True)

    @property
    def has_conviction(self) -> bool:
        return not self.convictions.empty

    @property
    def has_class_b_felony(self) -> bool:
        return self.convictions.has_any(FelonyClassB)

    @property
    def has_class_c_felony(self) -> bool:
        return self.convictions.has_any([FelonyClassC, "Felony Class C"])

    @property
    def has_class_a_misdemeanor(self) -> bool:
        return self.convictions.has_any([MisdemeanorClassA, "Misdemeanor Class A"])

    @property
    def has_class_bc_misdemeanor(self) -> bool:
        return self.convictions.has_any(MisdemeanorClassBC)

    @property
    def has_violation_or_contempt_of_court(self) -> bool:
        return self.convictions.has_any([Violation, ReducedToViolation, ContemptOfCourt, MarijuanaViolation])

    @property
    def has_probation_revoked(self) -> bool:
        return self.convictions.has_any_with_getter(lambda charge: charge.probation_revoked)


# https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html
# https://akdux.com/python/2020/10/31/python-fill-pdf-files/
# https://stackoverflow.com/questions/60082481/how-to-edit-checkboxes-and-save-changes-in-an-editable-pdf-using-the-python-pdfr

# * The PDF fields can be manually named using Acrobat and the source_data
# property can be inferred from the field name. For example, a field labeled
# "Full Name" will be mapped to `source_data.full_name`.

# However, PDF annotation fields should have unique names. So for forms that have repeat
# field names, append `---[unique_character_sequence]` to the field name. Ex:
# "Full Name---2" will also be mapped to `source_data.full_name`. (The `unique_character_sequence`
# does not affect the source_data mapping.)

# * If a value is not found, the supplementary mapping will be used.

# * When testing, test in Chrome, Firefox, Safari, Apple Preview and Acrobat Reader.
# Chrome and Firefox seem to have similar behavior while Safari and Apple Preview behvave similarly.
# For example, Apple will show a checked AcroForm checkbox field when an annotation's AP has been set to ""
# while Chrome and Firefox won't.


# Note: when printing pdfrw objects to screen during debugging, not all attributes are displayed. Stream objects
# can have many more nested properties.
class PDFFieldMapper(UserDict):
    STRING_FOR_DUPLICATES = "---"

    def __init__(self, pdf_source_path: str, source_data: UserInfo):
        super().__init__()

        self.pdf_source_path = pdf_source_path
        self.source_data = source_data
        self.data = self.extra_mappings()

    def __getitem__(self, key):
        attr = key[1:-1].lower().replace(" ", "_").split(self.STRING_FOR_DUPLICATES)[0]

        if hasattr(self.source_data, attr):
            return getattr(self.source_data, attr)
        else:
            return super().__getitem__(key)

    """
    The oregon.pdf mapping is mapped here instead of the PDF itself. Hopefully, future
    updates to the form from the state will leave most of the fields intact and
    only a few would need to be remapped.
    Process to create the extra mapping:
    1. Open the PDF in Acrobat.
    2. Click on "Prepare Form". This will add all of the form's fields and
       make them available via Root.AcroForm.Fields and the PDF's annotations.
    3. Adjust any fields as necessary, ex. move "(Address)" up to the
       correct line.
       * Sometimes a AcroForm.Field is created, but no annotation
       is assocated with it, ex "undefined" field that has no label. In this
       case, delete the field and create a new text field via the
       "Add a new text field" button.
       * If there are fields with the same names, then they wont' get annotations
       and would need to be renamed.
       * If adjusting a field after the file has been saved then the field value
       might not be displayed. Try recreating the field.
       * When something's not working recreate the field.
       * If a field is not wide enough, try to increase the height and make it a
       multiline field (Text Properties > Options.)
    4. Save the PDF.
    """

    def extra_mappings(self):
        s = self.source_data
        if not isinstance(s, CaseResults):
            # Is the OSP Form
            osp_fields: Dict[str, object] = {}
            for i in range(10):
                osp_fields[f"(Court {i+1})"] = f"Circuit Court for {s.counties_with_cases_to_expunge[i]} County" if i<len(s.counties_with_cases_to_expunge) else ""
            if s.has_eligible_convictions:
                osp_fields["(Include a Conviction Yes)"] = True
            else:
                osp_fields["(Include a Conviction No)"] = True
            return osp_fields
        return {
            "(FOR THE COUNTY OF)": s.county,
            "(Plaintiff)": "State of Oregon",
            "(Case No)": s.case_number_with_comments,
            "(Defendant)": s.case_name,
            "(DOB)": s.date_of_birth,
            "(record of arrest with no charges filed)": s.has_no_complaint,
            "(record of arrest with charges filed and the associated check all that apply)": not s.has_no_complaint,
            "(conviction)": s.has_conviction,
            "(record of citation or charge that was dismissedacquitted)": s.has_dismissed,
            "(contempt of court finding)": s.has_contempt_of_court,
            "(I am not currently charged with a crime)": True,
            "(The arrest or citation I want to set aside is not for a charge of Driving Under the Influence of)": True,
            "(Date of conviction contempt finding or judgment of GEI)": s.conviction_dates,
            "(ORS 137225 does not prohibit a setaside of this conviction see Instructions)": s.has_conviction,
            "(Felony  Class B and)": s.has_class_b_felony,
            "(Felony  Class C and)": s.has_class_c_felony,
            "(Misdemeanor  Class A and)": s.has_class_a_misdemeanor,
            "(Misdemeanor  Class B or C and)": s.has_class_bc_misdemeanor,
            "(Violation or Contempt of Court and)": s.has_violation_or_contempt_of_court,
            "(7 years have passed since the later of the convictionjudgment or release date and)": s.has_class_b_felony,
            "(I have not been convicted of any other offense or found guilty except for insanity in)": s.has_class_b_felony,
            "(5 years have passed since the later of the convictionjudgment or release date and)": s.has_class_c_felony,
            "(I have not been convicted of any other offense or found guilty except for insanity in_2)": s.has_class_c_felony,
            "(3 years have passed since the later of the convictionjudgment or release date and)": s.has_class_a_misdemeanor,
            "(I have not been convicted of any other offense or found guilty except for insanity in_3)": s.has_class_a_misdemeanor,
            "(1 year has passed since the later of the convictionfindingjudgment or release)": s.has_class_bc_misdemeanor,
            "(I have not been convicted of any other offense or found guilty except for insanity)": s.has_class_bc_misdemeanor,
            "(1 year has passed since the later of the convictionfindingjudgment or release_2)": s.has_violation_or_contempt_of_court,
            "(I have not been convicted of any other offense or found guilty except for insanity_2)": s.has_violation_or_contempt_of_court,
            "(I have fully completed complied with or performed all terms of the sentence of the court)": s.has_conviction,
            "(I was sentenced to probation in this case and)": s.has_probation_revoked,
            "(My probation WAS revoked and 3 years have passed since the date of revocation)": s.has_probation_revoked,
            "(Date of arrest)": s.arrest_dates,
            "(no accusatory instrument was filed and at least 60 days have passed since the)": s.has_no_complaint,
            "(an accusatory instrument was filed and I was acquitted or the case was dismissed)": s.has_dismissed,
            "(have sent)": True,
            "(Name typed or printed)": s.full_name,
            "(Address)": join_dates_or_strings(
                [s.mailing_address, s.city, s.state, s.zip_code, s.phone_number],
                connector=",    ",
                date_format="%b %-d, %Y",
            ),
            "(the District Attorney at address 2)": s.da_address,
            "(Name typed or printed_2)": s.full_name,
        }


class PDF:
    BUTTON_TYPE = "/Btn"
    BUTTON_ON = PdfName("On")
    BUTTON_YES = PdfName("Yes")
    TEXT_TYPE = "/Tx"
    FONT_FAMILY = "TimesNewRoman"
    FONT_SIZE = "10"
    FONT_SIZE_SMALL = "6"
    DATE_FORMAT = "%b %-d, %Y"
    STR_CONNECTOR = "; "

    @staticmethod
    def fill_form(mapper: PDFFieldMapper, should_validate=False):

        pdf = PDF(mapper)
        if should_validate:
            pdf.validate_initial_state()

        pdf.update_annotations()
        return pdf

    def __init__(self, mapper: PDFFieldMapper):
        self.set_pdf(PdfReader(mapper.pdf_source_path))
        self.mapper = mapper
        self.shrunk_fields: Dict[str, str] = {}
        self.writer = PdfWriter()

    def set_pdf(self, pdf: PdfReader):
        self._pdf = pdf
        self.annotations = [annot for page in self._pdf.pages for annot in page.Annots or []]
        self.fields = {field.T: field for field in self._pdf.Root.AcroForm.Fields}

    # Need to update both the V and AS fields of a Btn and they should be the same.
    # The value to use is found in annotation.AP.N.keys() and not
    # necessarily "/Yes". If a new form has been made, make sure to check
    # which value to use here and redefine BUTTON_ON if needed.
    def set_checkbox_on(self, annotation):
        if self.BUTTON_ON in annotation.AP.N.keys():
            annotation.V = self.BUTTON_ON
            annotation.AS = self.BUTTON_ON
        elif self.BUTTON_YES in annotation.AP.N.keys():
            annotation.V = self.BUTTON_YES
            annotation.AS = self.BUTTON_YES

    def set_text_value(self, annotation, value):
        new_value = value

        if isinstance(value, list):
            if len(value) == 0:
                return
            new_value = join_dates_or_strings(value, self.STR_CONNECTOR, self.DATE_FORMAT)

        annotation.V = PdfString.encode(new_value)
        self.set_font(annotation)
        annotation.update(PdfDict(AP=""))

    def set_font(self, annotation):
        x1, x2 = float(annotation.Rect[0]), float(annotation.Rect[2])
        max_chars = (x2 - x1) * 0.3125  # Times New Roman size 10
        num_chars = len(annotation.V) - 2  # minus parens
        font_size = self.FONT_SIZE

        if num_chars > max_chars:
            font_size = self.FONT_SIZE_SMALL
            self.shrunk_fields[annotation.T] = annotation.V

        annotation.DA = PdfString.encode(f"/{self.FONT_FAMILY} {font_size} Tf 0 g")

    def update_annotations(self):
        for annotation in self.annotations:
            new_value = self.mapper.get(annotation.T)

            if annotation.FT == self.BUTTON_TYPE and new_value:
                self.set_checkbox_on(annotation)

            if annotation.FT == self.TEXT_TYPE and new_value is not None:
                self.set_text_value(annotation, new_value)

        self._pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))

    def add_text(self, text: str):
        _pdf = PdfReader(fdata=MarkdownToPDF.to_pdf("Addendum", text))
        self.writer.addpages(_pdf.pages)

    def write(self, path: str):
        self.writer.addpages(self._pdf.pages)

        trailer = self.writer.trailer
        trailer.Root.AcroForm = self._pdf.Root.AcroForm

        self.writer.write(path, trailer=trailer)

    def get_annotation_dict(self):
        return {anot.T: anot for anot in self.annotations}

    def get_annotation_values(self):
        return {anot.T: anot.V for anot in self.annotations}

    def get_field_dict(self):
        return {field.T: field.V for field in self._pdf.Root.AcroForm.Fields}

    def validate_initial_state(self):
        not_blank_message = lambda elem, type: f"[PDF] PDF {type} not blank: {elem.T} - {elem.V}"

        for field in self._pdf.Root.AcroForm.Fields:
            assert field.V in [None, "/Off", "()"], not_blank_message(field, "field")

        for annotation in self.annotations:
            assert annotation.V in [None, "/Off", "()"], not_blank_message(annotation, "annotation")

        assert set(self.get_field_dict()) == set(
            self.get_annotation_dict()
        ), "[PDF] PDF fields do not match annotations"


class FormFilling:
    OREGON_PDF_NAME = "oregon"
    NON_OREGON_PDF_COUNTIES = ["multnomah"]
    COUNTIES_NEEDING_CONVICTION_OR_ARREST_ORDER = ["douglas", "umatilla", "multnomah"]
    COUNTIES_NEEDING_COUNTY_SPECIFIC_DOWNLOAD_NAME = ["douglas", "umatilla"]
    OSP_PDF_NAME = "OSP_Form"

    @staticmethod
    def build_zip(record_summary: RecordSummary, user_information_dict: Dict[str, str]) -> Tuple[str, str]:
        temp_dir = mkdtemp()
        zip_file_name = "expungement_packet.zip"
        zip_path = path.join(mkdtemp(), zip_file_name)
        zip_file = ZipFile(zip_path, "w")

        sid = FormFilling._unify_sids(record_summary)

        all_case_results = []
        has_eligible_convictions = False
        for case in record_summary.record.cases:
            case_results = CaseResults.build(case, user_information_dict, sid)

            if case_results.get_has_eligible_convictions:
                has_eligible_convictions = True
            all_case_results.append(case_results)
            if case_results.is_expungeable_now:
                file_info = FormFilling._create_and_write_pdf(case_results, temp_dir)
                zip_file.write(*file_info)
        user_information_dict_2: Dict[str, object] = {**user_information_dict}
        user_information_dict_2["counties_with_cases_to_expunge"] = FormFilling.counties_with_cases_to_expunge(
            all_case_results
        )
        user_information_dict_2["has_eligible_convictions"] = has_eligible_convictions
        osp_file_info = FormFilling._create_and_write_pdf(user_information_dict_2, temp_dir)
        zip_file.write(*osp_file_info)
        zip_file.close()

        return zip_path, zip_file_name

    @staticmethod
    def _unify_sids(record_summary: RecordSummary) -> str:
        """
        We just take the first non-empty SID for now.
        """
        for case in record_summary.record.cases:
            if case.summary.sid:
                return case.summary.sid
        return ""

    @staticmethod
    def _generate_warnings_text(shrunk_fields: Dict[str, str], mapper: PDFFieldMapper) -> Optional[str]:
        text = None
        warnings: List[str] = []

        if mapper.get("(has_ineligible_charges)"):
            message = "This form will attempt to expunge a case in part. This is relatively rare, and thus these forms should be reviewed particularly carefully."
            warnings.append(message)

        if shrunk_fields:
            for field_name, value in shrunk_fields.items():
                message = f'* The font size of "{value[1:-1]}" was shrunk to fit the bounding box of "{field_name[1:-1]}". An addendum might be required if it still doesn\'t fit.'
                warnings.append(message)

        if warnings:
            text = "# Warnings from RecordSponge  \n"
            text += "Do not submit this page to the District Attorney's office.  \n \n"
            for warning in warnings:
                text += f"\* {warning}  \n"

        return text

    @staticmethod
    def _build_download_file_path(download_dir: str, source_data: Union[UserInfo, CaseResults]) -> Tuple[str, str]:
        if isinstance(source_data, CaseResults):
            base_name = source_data.county.lower()

            if base_name in FormFilling.COUNTIES_NEEDING_COUNTY_SPECIFIC_DOWNLOAD_NAME:
                base_name += "_with_"
                base_name += "conviction" if source_data.has_conviction else "arrest"
                base_name += "_order"

            file_name = f"{source_data.case_name}_{source_data.case_number}_{base_name}"
        else:
            file_name = FormFilling.OSP_PDF_NAME

        file_name += ".pdf"

        return path.join(download_dir, file_name), file_name

    @staticmethod
    def _get_pdf_file_name(source_data: Union[UserInfo, CaseResults]) -> str:
        if isinstance(source_data, CaseResults):
            county = source_data.county.lower()
            file_name = county if county in FormFilling.NON_OREGON_PDF_COUNTIES else FormFilling.OREGON_PDF_NAME

            if county in FormFilling.COUNTIES_NEEDING_CONVICTION_OR_ARREST_ORDER:
                file_name += "_conviction" if source_data.has_conviction else "_arrest"
        else:
            file_name = FormFilling.OSP_PDF_NAME

        return file_name + ".pdf"

    @staticmethod
    def _create_pdf(source_data: UserInfo, validate_initial_pdf_state=False) -> PDF:
        file_name = FormFilling._get_pdf_file_name(source_data)
        source_dir = path.join(Path(__file__).parent, "files")
        pdf_path = path.join(source_dir, file_name)

        mapper = PDFFieldMapper(pdf_path, source_data)
        return PDF.fill_form(mapper, validate_initial_pdf_state)

    @staticmethod
    def _create_and_write_pdf(
        data: Union[Dict, UserInfo], dir: str, validate_initial_pdf_state=False
    ) -> Tuple[str, str]:
        if isinstance(data, UserInfo):
            source_data = data
        else:
            source_data = UserInfo(**data)

        pdf = FormFilling._create_pdf(source_data, validate_initial_pdf_state)
        warnings_text = FormFilling._generate_warnings_text(pdf.shrunk_fields, pdf.mapper)

        if warnings_text:
            pdf.add_text(warnings_text)

        write_file_path, write_file_name = FormFilling._build_download_file_path(dir, source_data)
        pdf.write(write_file_path)

        return write_file_path, write_file_name

    @staticmethod
    def counties_with_cases_to_expunge(all_case_results: List[CaseResults]):
        counties_with_eligible_charge: List[str] = []
        counties_with_balances: List[str] = []
        for case_result in all_case_results:
            if case_result.has_eligible_charges and case_result.case.summary.location not in counties_with_eligible_charge:
                counties_with_eligible_charge.append(case_result.case.summary.location)
            if case_result.case.summary.balance_due_in_cents != 0:
                counties_with_balances.append(case_result.case.summary.location)
        counties_with_expungements = [county for county in counties_with_eligible_charge if county not in counties_with_balances]
        return counties_with_expungements
