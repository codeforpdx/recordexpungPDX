import os
from dataclasses import dataclass, replace
from os import path
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Dict, Tuple, Optional
from zipfile import ZipFile

from dacite import from_dict
from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaViolation, MarijuanaEligible
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.record_summary import RecordSummary
from expungeservice.old_form_filling import FormFilling as OldFormFilling
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject


@dataclass
class FormData:
    county: str
    case_number: str
    case_name: str
    da_number: str
    sid: str

    has_conviction: str
    has_no_complaint: str
    has_dismissed: str
    has_contempt_of_court: str
    conviction_dates: str

    has_class_b_felony: str
    has_class_c_felony: str
    has_class_a_misdemeanor: str
    has_class_bc_misdemeanor: str
    has_violation_or_contempt_of_court: str
    has_probation_revoked: str

    dismissed_arrest_dates: str
    arresting_agency: str

    date_of_birth: str
    full_name: str
    mailing_address: str
    phone_number: str
    city: str
    state: str
    zip_code: str

    da_address: str


@dataclass
class CertificateFormData:
    full_name: str
    date_of_birth: str
    phone_number: str
    mailing_address: str
    city: str
    state: str
    zip_code: str


class FormFilling:
    @staticmethod
    def build_zip(record_summary: RecordSummary, user_information: Dict[str, str]) -> Tuple[str, str]:
        temp_dir = mkdtemp()
        zip_dir = mkdtemp()
        zip_name = "expungement_packet.zip"
        zip_path = path.join(zip_dir, zip_name)
        zipfile = ZipFile(zip_path, "w")
        for case in record_summary.record.cases:
            case_without_deleted_charges = replace(
                case, charges=tuple(c for c in case.charges if c.edit_status != EditStatus.DELETE)
            )
            pdf_with_warnings = FormFilling._build_pdf_for_case(case_without_deleted_charges, user_information)
            if pdf_with_warnings:
                pdf, internal_file_name, warnings = pdf_with_warnings
                file_name = f"{case_without_deleted_charges.summary.name}_{case_without_deleted_charges.summary.case_number}_{internal_file_name}"
                file_path = path.join(temp_dir, file_name)
                writer = PdfWriter()
                writer.addpages(pdf.pages)
                FormFilling._add_warnings(writer, warnings)
                trailer = writer.trailer
                trailer.Root.AcroForm = pdf.Root.AcroForm
                writer.write(file_path, trailer=trailer)
                zipfile.write(file_path, file_name)

        # TODO: Extract to method
        pdf = FormFilling._build_certificate_of_mailing_pdf(user_information)
        file_name = f"certificate_of_mailing.pdf"
        file_path = path.join(temp_dir, file_name)
        writer = PdfWriter()
        writer.addpages(pdf.pages)
        trailer = writer.trailer
        trailer.Root.AcroForm = pdf.Root.AcroForm
        writer.write(file_path, trailer=trailer)
        zipfile.write(file_path, file_name)

        # TODO: Remove
        old_zip_path, old_zip_name = OldFormFilling.build_zip(record_summary, user_information)
        zipfile.write(old_zip_path, old_zip_name)

        zipfile.close()
        return zip_path, zip_name

    @staticmethod
    def _build_certificate_of_mailing_pdf(user_information: Dict[str, str]) -> PdfReader:
        form = from_dict(data_class=CertificateFormData, data=user_information)
        pdf_path = path.join(Path(__file__).parent, "files", f"certificate_of_mailing.pdf")
        pdf = PdfReader(pdf_path)
        for field in pdf.Root.AcroForm.Fields:
            field_name = field.T.lower().replace(" ", "_").replace("(", "").replace(")", "")
            field_value = getattr(form, field_name)
            field.V = field_value
        for page in pdf.pages:
            annotations = page.get("/Annots")
            if annotations:
                for annotation in annotations:
                    annotation.update(PdfDict(AP=""))
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
        return pdf

    @staticmethod
    def _add_warnings(writer: PdfWriter, warnings: List[str]):
        if warnings:
            text = "# Warnings from RecordSponge  \n"
            text += "Do not submit this page to the District Attorney's office.  \n \n"
            for warning in warnings:
                text += f"\* {warning}  \n"
            blank_pdf_bytes = MarkdownToPDF.to_pdf("Addendum", text)
            blank_pdf = PdfReader(fdata=blank_pdf_bytes)
            writer.addpages(blank_pdf.pages)

    @staticmethod
    def _build_pdf_for_case(case: Case, user_information: Dict[str, str]) -> Optional[Tuple[PdfReader, str, List[str]]]:
        eligible_charges, ineligible_charges = Case.partition_by_eligibility(case.charges)
        in_part = ", ".join([charge.ambiguous_charge_id.split("-")[-1] for charge in eligible_charges])
        case_number_with_comments = (
            f"{case.summary.case_number} (in part - counts {in_part})"
            if ineligible_charges
            else case.summary.case_number
        )
        if eligible_charges:
            pdf, file_name, warnings = FormFilling._build_pdf_for_eligible_case(
                case, eligible_charges, user_information, case_number_with_comments
            )
            if ineligible_charges:
                warnings.insert(
                    0,
                    "This form will attempt to expunge a case in part. This is relatively rare, and thus these forms should be reviewed particularly carefully.",
                )
            return pdf, file_name, warnings
        else:
            return None

    @staticmethod
    def _build_pdf_for_eligible_case(
        case: Case, eligible_charges: List[Charge], user_information: Dict[str, str], case_number_with_comments: str
    ) -> Tuple[PdfReader, str, List[str]]:
        warnings: List[str] = []
        dismissals, convictions = Case.categorize_charges(eligible_charges)
        dismissed_arrest_dates = list(set([charge.date.strftime("%b %-d, %Y") for charge in dismissals]))
        conviction_dates = list(set([charge.disposition.date.strftime("%b %-d, %Y") for charge in convictions]))
        has_conviction = len(convictions) > 0
        has_dismissals = len(dismissals) > 0
        has_no_complaint = any([charge.no_complaint() for charge in dismissals])
        has_contempt_of_court = any([isinstance(charge.charge_type, ContemptOfCourt) for charge in eligible_charges])

        # TODO: Fix MJ Eligible to be in its proper class
        has_class_b_felony = any([isinstance(charge.charge_type, FelonyClassB) for charge in convictions])
        has_class_c_felony = any(
            [
                isinstance(charge.charge_type, FelonyClassC) or isinstance(charge.charge_type, MarijuanaEligible)
                for charge in convictions
            ]
        )
        has_class_a_misdemeanor = any([isinstance(charge.charge_type, MisdemeanorClassA) for charge in convictions])
        has_class_bc_misdemeanor = any([isinstance(charge.charge_type, MisdemeanorClassBC) for charge in convictions])
        has_violation_or_contempt_of_court = any(
            [
                isinstance(charge.charge_type, Violation)
                or isinstance(charge.charge_type, ReducedToViolation)
                or isinstance(charge.charge_type, ContemptOfCourt)
                or isinstance(charge.charge_type, MarijuanaViolation)
                for charge in convictions
            ]
        )
        has_probation_revoked = any([charge.probation_revoked for charge in convictions])

        da_address = FormFilling._build_da_address(case.summary.location)

        form_data_dict = {
            **user_information,
            "county": case.summary.location,
            "case_number": case_number_with_comments,
            "case_name": case.summary.name,
            "da_number": case.summary.district_attorney_number,
            "sid": case.summary.sid,
            "has_conviction": "✓" if has_conviction else "",
            "has_no_complaint": "✓" if has_no_complaint else "",
            "has_dismissed": "✓" if has_dismissals else "",
            "has_contempt_of_court": "✓" if has_contempt_of_court else "",
            "conviction_dates": "; ".join(conviction_dates),
            "has_class_b_felony": "✓" if has_class_b_felony else "",
            "has_class_c_felony": "✓" if has_class_c_felony else "",
            "has_class_a_misdemeanor": "✓" if has_class_a_misdemeanor else "",
            "has_class_bc_misdemeanor": "✓" if has_class_bc_misdemeanor else "",
            "has_violation_or_contempt_of_court": "✓" if has_violation_or_contempt_of_court else "",
            "has_probation_revoked": "✓" if has_probation_revoked else "",
            "dismissed_arrest_dates": "; ".join(dismissed_arrest_dates),
            "arresting_agency": "",
            "da_address": da_address,
        }
        form = from_dict(data_class=FormData, data=form_data_dict)
        pdf_path = path.join(Path(__file__).parent, "files", f"oregon.pdf")
        file_name = os.path.basename(pdf_path)
        pdf = PdfReader(pdf_path)
        for field in pdf.Root.AcroForm.Fields:
            field_name = field.T.lower().replace(" ", "_").replace("(", "").replace(")", "")
            field_value = getattr(form, field_name)
            field.V = field_value
            warnings += FormFilling._set_font(field, field_value)
        for page in pdf.pages:
            annotations = page.get("/Annots")
            if annotations:
                for annotation in annotations:
                    annotation.update(PdfDict(AP=""))
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
        return pdf, file_name, warnings

    @staticmethod
    def _set_font(field: PdfDict, field_value: str) -> List[str]:
        warnings: List[str] = []
        if field["/Kids"]:
            for kid in field["/Kids"]:
                FormFilling._set_font_for_field(field, field_value, kid, warnings)
        else:
            FormFilling._set_font_for_field(field, field_value, field, warnings)
        return warnings

    @staticmethod
    def _set_font_for_field(field, field_value, kid, warnings):
        font_string, needs_shrink = FormFilling._build_font_string(kid, field_value)
        kid.DA = font_string
        if needs_shrink:
            message = f'The font size of "{field.V}" was shrunk to fit the bounding box of "{field.T}". An addendum might be required if it still doesn\'t fit.'
            warnings.append(message)

    @staticmethod
    def _build_font_string(field: PdfDict, field_value: str) -> Tuple[str, bool]:
        max_length = FormFilling._compute_field_max_length(field)
        needs_shrink = len(field_value) > max_length
        font_size = 6 if needs_shrink else 8
        return f"/TimesNewRoman  {font_size} Tf 0 g", needs_shrink

    @staticmethod
    def _compute_field_max_length(field: PdfDict) -> int:
        CHARACTER_WIDTH = 0.25  # Times New Roman size 8
        width = float(field.Rect[2]) - float(field.Rect[0])
        return int(width * CHARACTER_WIDTH)

    @staticmethod
    def _build_da_address(location: str) -> str:
        ADDRESSES = {
            "Baker": "Baker County Courthouse - 1995 Third Street, Suite 320 - Baker City, OR 97814",
            "Benton": "District Attorney's Office - 120 NW 4th St. - Corvallis, OR 97330",
            "Clackamas": "807 Main Street - Oregon City, OR 97045",
            "Clatsop": "Clatsop County District Attorney’s Office - PO Box 149 - Astoria, OR 97103",
            "Columbia": "230 Strand St. - Columbia County Courthouse Annex - St. Helens, OR 97051",
            "Coos": "Coos County District Attorney's Office - 250 N. Baxter - Coquille, Oregon 97423",
            "Crook ": "District Attorney - 300 NE 3rd St, Rm. 34 - Prineville, OR 97754",
            "Deschutes": "District Attorney - 1164 NW Bond St. - Bend, OR 97703",
            "Douglas": "District Attorney - 1036 SE Douglas Avenue - Justice Building, Room 204 - Roseburg, OR 97470",
            "Gilliam": "District Attorney - 221 S. Oregon St - PO Box 636 - Condon, OR 97823",
            "Grant": "District Attorney - 201 South Humbolt Street - Canyon City, Oregon, 97820",
            "Harney": "District Attorney - 450 N Buena Vista Ave - Burns, OR 97720",
            "Hood River": "District Attorney - 309 State Street  - Hood River, OR 97031",
            "Jackson": "District Attorney - 815 W. 10th Street - Medford, Oregon 97501",
            "Jefferson": "District Attorney - 129 SW E Street, Suite 102 - Madras, Oregon 97741",
            "Josephine": "District Attorney - 500 NW 6th St #16 - Grants Pass, OR 97526",
            "Klamath": "District Attorney - 305 Main Street - Klamath Falls, OR 97601",
            "Lake": "District Attorney - 513 Center St, Lakeview, OR 97630",
            "Lane": "District Attorney - 125 E 8th Ave - Eugene, OR 97401",
            "Lincoln": "District Attorney - 225 W Olive St # 100 - Newport, OR 97365",
            "Linn": "District Attorney - PO Box 100 - Albany, Oregon 97321",
            "Malheur": "District Attorney - 251 B St. West #6 - Vale, OR 97918",
            "Marion": "District Attorney - PO Box 14500 - Salem, OR 97309",
            "Morrow": "District Attorney - P.O. Box 664 - Heppner, OR  97836",
            "Multnomah": "Multnomah County Central Courthouse - 1200 S.W. 1st Avenue, Suite 5200 - Portland, Oregon 97204",
            "Polk": "District Attorney - 850 Main Street - Dallas, OR 97338",
            "Sherman": "District Attorney - P.O. Box 393 - Moro, OR 97039",
            "Tillamook": "District Attorney - 201 Laurel Ave - Tillamook, OR 97141",
            "Umatilla": "District Attorney - 216 SE Court Ave #3 - Pendleton, OR 97801",
            "Union": "District Attorney - 1104 K Ave - La Grande, OR 97850",
            "Wallowa": "District Attorney - 101 S. River Street, Rm. 201 - Enterprise, OR 97828",
            "Wasco": "District Attorney - 511 Washington St #304 - The Dalles, OR 97058",
            "Washington": "District Attorney - 150 N First Avenue, Suite 300 - Hillsboro, OR 97124-3002",
            "Wheeler": "District Attorney - P.O. Box 512 - Fossil, OR 97830",
            "Yamhill": "District Attorney - 535 NE 5th St #117 - McMinnville, OR 97128",
        }
        return ADDRESSES[location]
