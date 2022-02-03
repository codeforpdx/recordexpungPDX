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
from expungeservice.models.record_summary import RecordSummary
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject


@dataclass
class FormData:
    case_name: str
    case_number: str
    case_number_with_comments: str  # For legacy reasons; same as case_number
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
        zip_name = "old_expungement_packet.zip"
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
        zipfile.close()
        return zip_path, zip_name

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
        charges = case.charges
        charge_names = [charge.name.title() for charge in charges]
        arrest_dates_all = list(set([charge.date.strftime("%b %-d, %Y") for charge in charges]))
        dismissals, convictions = Case.categorize_charges(eligible_charges)
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
            "case_number": case_number_with_comments,
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
        location = case.summary.location.lower()
        warning = FormFilling._warn_charge_count_overflow(location, convictions, dismissals)
        if warning:
            warnings.append(warning)
        pdf_path = FormFilling._build_pdf_path(location, convictions)
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
    def _build_six_charges(charges: List[Charge]) -> Dict[str, str]:
        acc: Dict[str, str] = {}
        for i in range(1, 7):
            acc = {**acc, **FormFilling._build_charge(charges, i)}
        return acc

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
    def _warn_charge_count_overflow(
        location: str, convictions: List[Charge], dismissals: List[Charge]
    ) -> Optional[str]:
        JACKSON_CONVICTION_SLOTS = 6
        JACKSON_ARREST_SLOTS = 3
        MARION_CONVICTION_SLOTS = 3
        MARION_ARREST_SLOTS = 4
        POLK_CONVICTION_SLOTS = 3
        POLK_ARREST_SLOTS = 3

        def conviction_message(slots):
            return f"This case has {all_count} eligible charges. Since this form only has {slots} slots, the remaining charges will need to be written in an addendum. A separate addendum is needed for the motion and the order."

        def dismissal_message(slots):
            return f"This case has {dismissal_count} eligible dismissed/acquitted charges. Since this form only has {slots} slots, the remaining charges will need to be written in an addendum. A separate addendum is needed for the motion and the order."

        all_count = len(convictions + dismissals)
        dismissal_count = len(dismissals)
        if convictions:
            if location == "jackson" and all_count > JACKSON_CONVICTION_SLOTS:
                return conviction_message(JACKSON_CONVICTION_SLOTS)
            elif location == "marion" and all_count > MARION_CONVICTION_SLOTS:
                return conviction_message(MARION_CONVICTION_SLOTS)
            elif location == "polk" and all_count > POLK_CONVICTION_SLOTS:
                return conviction_message(POLK_CONVICTION_SLOTS)
        else:
            if location == "jackson" and all_count > JACKSON_ARREST_SLOTS:
                return dismissal_message(JACKSON_ARREST_SLOTS)
            elif location == "marion" and all_count > MARION_ARREST_SLOTS:
                return dismissal_message(MARION_ARREST_SLOTS)
            elif location == "polk" and all_count > POLK_ARREST_SLOTS:
                return dismissal_message(POLK_ARREST_SLOTS)
        return None

    @staticmethod
    def _build_pdf_path(location: str, convictions: List[Charge]) -> str:
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
