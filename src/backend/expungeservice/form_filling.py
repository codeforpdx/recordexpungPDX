from dataclasses import dataclass, replace
from os import path
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Dict, Tuple, Optional
from zipfile import ZipFile

from dacite import from_dict
from expungeservice.expunger import Expunger
from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record_summary import RecordSummary

from more_itertools import partition
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject


@dataclass
class FormData:
    case_name: str
    case_number: str
    case_number_with_comments: str  # For Clackamas and Lincoln county
    da_number: str
    full_name: str
    date_of_birth: str
    mailing_address: str
    phone_number: str
    city: str
    state: str
    zip_code: str
    arresting_agency: str

    arrest_dates_all: str
    charges_all: str

    eligible_arrest_dates_all: str
    eligible_charges_all: str

    dismissed_charges: str
    dismissed_arrest_dates: str
    dismissed_dates: str

    conviction_charges: str
    conviction_arrest_dates: str
    conviction_dates: str

    dispositions: str

    defendant_name: str
    county: str

    charge_1: str
    charge_1_arrest_date: str
    charge_1_agency: str
    charge_1_disposition: str
    charge_1_disposition_date: str

    charge_2: str
    charge_2_arrest_date: str
    charge_2_agency: str
    charge_2_disposition: str
    charge_2_disposition_date: str

    charge_3: str
    charge_3_arrest_date: str
    charge_3_agency: str
    charge_3_disposition: str
    charge_3_disposition_date: str

    charge_4: str
    charge_4_arrest_date: str
    charge_4_agency: str
    charge_4_disposition: str
    charge_4_disposition_date: str

    charge_5: str
    charge_5_arrest_date: str
    charge_5_agency: str
    charge_5_disposition: str
    charge_5_disposition_date: str

    charge_6: str
    charge_6_arrest_date: str
    charge_6_agency: str
    charge_6_disposition: str
    charge_6_disposition_date: str


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
            pdf = FormFilling._build_pdf_for_case(case_without_deleted_charges, user_information)
            if pdf:
                file_name = f"{case_without_deleted_charges.summary.name}_{case_without_deleted_charges.summary.case_number}.pdf"
                file_path = path.join(temp_dir, file_name)
                PdfWriter().write(file_path, pdf)
                zipfile.write(file_path, file_name)
        zipfile.close()
        return zip_path, zip_name

    @staticmethod
    def _build_pdf_for_case(case: Case, user_information: Dict[str, str]) -> Optional[PdfReader]:
        ineligible_charges_generator, eligible_charges_generator = partition(
            lambda c: c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
            if c.expungement_result.charge_eligibility
            else False,
            case.charges,
        )
        ineligible_charges, eligible_charges = list(ineligible_charges_generator), list(eligible_charges_generator)
        in_part = ", ".join(
            [charge.ambiguous_charge_id.split("-")[-1] for charge in eligible_charges]
        )  # TODO: Check if compatible with edit feature
        case_number_with_comments = (
            f"{case.summary.case_number} (in part - counts {in_part})"
            if ineligible_charges
            else case.summary.case_number
        )
        if eligible_charges:
            return FormFilling._build_pdf_for_eligible_case(
                case, eligible_charges, user_information, case_number_with_comments
            )
        else:
            return None

    @staticmethod
    def _build_pdf_for_eligible_case(
        case: Case, eligible_charges: List[Charge], user_information: Dict[str, str], case_number_with_comments: str
    ) -> PdfReader:
        charges = case.charges
        charge_names = [charge.name.title() for charge in charges]
        arrest_dates_all = list(set([charge.date.strftime("%b %-d, %Y") for charge in charges]))
        dismissals, convictions = Expunger._categorize_charges(eligible_charges)
        dismissed_names = [charge.name.title() for charge in dismissals]
        dismissed_arrest_dates = list(set([charge.date.strftime("%b %-d, %Y") for charge in dismissals]))
        dismissed_dates = list(set([charge.disposition.date.strftime("%b %-d, %Y") for charge in dismissals]))
        conviction_names = [charge.name.title() for charge in convictions]
        conviction_arrest_dates = list(set([charge.date.strftime("%b %-d, %Y") for charge in convictions]))
        conviction_dates = list(set([charge.disposition.date.strftime("%b %-d, %Y") for charge in convictions]))
        eligible_arrest_dates_all = list(set(dismissed_arrest_dates + conviction_arrest_dates))
        eligible_charge_names = dismissed_names + conviction_names
        dismissed_dispositions = ", ".join(dismissed_names) + " - Dismissed; " if dismissed_names else ""
        conviction_dispositions = ", ".join(conviction_names) + " - Convicted" if conviction_names else ""
        dispositions = dismissed_dispositions + conviction_dispositions
        form_data_dict = {
            **user_information,
            "case_name": case.summary.name,
            "case_number": case.summary.case_number,
            "case_number_with_comments": case_number_with_comments,
            "da_number": case.summary.district_attorney_number,
            "arresting_agency": "",
            "arrest_dates_all": "; ".join(arrest_dates_all),
            "charges_all": "; ".join(charge_names),
            "eligible_arrest_dates_all": "; ".join(eligible_arrest_dates_all),
            "eligible_charges_all": "; ".join(eligible_charge_names),
            "dispositions": dispositions,
            "dismissed_charges": "; ".join(dismissed_names),
            "dismissed_arrest_dates": "; ".join(dismissed_arrest_dates),
            "dismissed_dates": "; ".join(dismissed_dates),
            "conviction_charges": "; ".join(conviction_names),
            "conviction_arrest_dates": "; ".join(conviction_arrest_dates),
            "conviction_dates": "; ".join(conviction_dates),
            "defendant_name": case.summary.name,
            "county": case.summary.location,
            **FormFilling._build_six_charges(convictions + dismissals),
        }
        form = from_dict(data_class=FormData, data=form_data_dict)
        pdf_path = FormFilling._build_pdf_path(case, convictions)
        pdf = PdfReader(pdf_path)
        for field in pdf.Root.AcroForm.Fields:
            field_name = field.T.lower().replace(" ", "_").replace("(", "").replace(")", "")
            field_value = getattr(form, field_name)
            field.V = field_value
            FormFilling._set_font(field, field_value)
        for page in pdf.pages:
            annotations = page.get("/Annots")
            if annotations:
                for annotation in annotations:
                    annotation.update(PdfDict(AP=""))
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
        return pdf

    @staticmethod
    def _set_font(field: PdfDict, field_value: str) -> None:
        if field["/Kids"]:
            for kid in field["/Kids"]:
                font_string = FormFilling._build_font_string(kid, field_value)
                kid.DA = font_string
        else:
            font_string = FormFilling._build_font_string(field, field_value)
            field.DA = font_string

    @staticmethod
    def _build_font_string(field: PdfDict, field_value: str) -> str:
        max_length = FormFilling._compute_field_max_length(field)
        font_size = 6 if len(field_value) > max_length else 8
        return f"/TimesNewRoman  {font_size} Tf 0 g"

    @staticmethod
    def _compute_field_max_length(field: PdfDict) -> int:
        CHARACTER_WIDTH = 0.25  # Times New Roman size 8
        width = float(field.Rect[2]) - float(field.Rect[0])
        return int(width * CHARACTER_WIDTH)

    @staticmethod
    def _build_six_charges(charges: List[Charge]) -> Dict[str, str]:
        acc: Dict[str, str] = {}
        for i in range(1, 7):
            acc = {**acc, **FormFilling._build_charge(charges, i)}
        return acc

    # TODO: Double check case where disposition date is missing
    @staticmethod
    def _build_charge(charges: List[Charge], i: int) -> Dict[str, str]:
        if len(charges) > (i - 1):
            charge = charges[i - 1]
            return {
                f"charge_{i}": charge.name.title(),
                f"charge_{i}_arrest_date": charge.date.strftime("%b %-d, %Y"),
                f"charge_{i}_agency": "",
                f"charge_{i}_disposition": charge.disposition.ruling,
                f"charge_{i}_disposition_date": charge.disposition.date.strftime("%b %-d, %Y"),
            }
        else:
            return {
                f"charge_{i}": "",
                f"charge_{i}_arrest_date": "",
                f"charge_{i}_agency": "",
                f"charge_{i}_disposition": "",
                f"charge_{i}_disposition_date": "",
            }

    @staticmethod
    def _build_pdf_path(case: Case, convictions: List[Charge]) -> str:
        SUPPORTED_COUNTIES = [
            "multnomah",
            "jackson",
            "clackamas",
            "lane",
            "washington",
            "marion",
            "linn",
            "yamhill",
            "benton",
            "josephine",
            "polk",
            "tillamook",
            "lincoln",
            "umatilla",
            "coos",
            "baker",
            "curry",
            "morrow",
        ]
        location = case.summary.location.lower()
        if convictions:
            if location in SUPPORTED_COUNTIES:
                return path.join(Path(__file__).parent, "files", f"{location}_conviction.pdf")
            else:
                return path.join(Path(__file__).parent, "files", "stock_conviction.pdf")
        else:
            if location in SUPPORTED_COUNTIES:
                return path.join(Path(__file__).parent, "files", f"{location}_arrest.pdf")
            else:
                return path.join(Path(__file__).parent, "files", "stock_arrest.pdf")
