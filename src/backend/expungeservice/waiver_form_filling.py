from dataclasses import dataclass
from tempfile import mkdtemp
from os import path
from pathlib import Path
from typing import Dict, Tuple
from pdfrw import PdfReader, PdfDict, PdfString, PdfWriter, PdfName
from zipfile import ZipFile
from datetime import date

from expungeservice.models.record_summary import RecordSummary
from expungeservice.models.case import Case
from expungeservice.form_filling import DA_ADDRESSES

@dataclass
class CaseData:
    case: Case
    user_information_dict: Dict
    waiver_information_dict: Dict


def get_mapping(case_data: CaseData):
    benefit = case_data.waiver_information_dict["snap"] or case_data.waiver_information_dict["snap"] or case_data.waiver_information_dict["snap"] or case_data.waiver_information_dict["snap"]
    today = date.today().strftime("%b %-d, %Y")
    da_address_lines = DA_ADDRESSES[case_data.case.summary.location.lower()].split("-")
    mapping = {
        "(Case No)": case_data.case.summary.case_number,
        "(Defendant)":case_data.case.summary.name,
        "(Date)":today,
        "(County)":case_data.case.summary.location,
        "(Benefit)": benefit,
        "(SNAP)": case_data.waiver_information_dict["snap"],
        "(SSI)": case_data.waiver_information_dict["ssi"],
        "(TANF)": case_data.waiver_information_dict["tanf"],
        "(OHP)": case_data.waiver_information_dict["ohp"],
        "(Explain1)": case_data.waiver_information_dict["explain"][:70],
        "(Explain2)": case_data.waiver_information_dict["explain"][70:140],
        "(Explain3)": case_data.waiver_information_dict["explain"][140:210],
        "(Explain4)": case_data.waiver_information_dict["explain"][210:280],
        "(Ask1)": case_data.waiver_information_dict["explain2"][:70],
        "(Ask2)": case_data.waiver_information_dict["explain2"][70:140],
        "(Ask3)": case_data.waiver_information_dict["explain2"][140:210],
        "(Ask4)": case_data.waiver_information_dict["explain2"][210:270],
        "(Custody)": case_data.waiver_information_dict["custody"],
        "(Name)": case_data.user_information_dict["full_name"],
        "(Address)": case_data.user_information_dict["mailing_address"],
        "(CityStateZip)": f"{case_data.user_information_dict['city']}, {case_data.user_information_dict['state']} {case_data.user_information_dict['zip_code']}",
        "(Phone)": case_data.user_information_dict["phone_number"],
        "(Date2)": today,
        "(DaAddress1)": da_address_lines[0],
        "(DaAddress2)": da_address_lines[1],
        "(DaAddress3)": da_address_lines[2] if len(da_address_lines) > 2 else "",
        "(Name2)":case_data.user_information_dict["full_name"],
        "(Date3)":today
    }
    return mapping

class WaiverFormFilling:
    COUNTIES_WITHOUT_WAIVER_PROGRAM = ["multnomah"]

    @staticmethod
    def build_zip(
        record_summary: RecordSummary, user_information_dict: Dict[str, str], waiver_information_dict
    ) -> Tuple[str, str]:
        temp_dir = mkdtemp()
        zip_file_name = "waiver_packet.zip"
        zip_path = path.join(mkdtemp(), zip_file_name)
        zip_file = ZipFile(zip_path, "w")

        for case in record_summary.record.cases:

            if (
                case.summary.balance_due_in_cents > 0
                and case.summary.location not in WaiverFormFilling.COUNTIES_WITHOUT_WAIVER_PROGRAM
            ):
                case_data = CaseData(case, user_information_dict, waiver_information_dict)
                file_info = WaiverFormFilling._create_and_write_pdf(case_data, temp_dir)
                zip_file.write(*file_info[0:2])

        zip_file.close()

        return zip_path, zip_file_name

    @staticmethod
    def _create_and_write_pdf(case_data: CaseData, temp_dir: str):
        file_name = "fee_waiver.pdf"
        source_dir = path.join(Path(__file__).parent, "files")
        pdf_path = path.join(source_dir, file_name)
        pdf = PdfReader(pdf_path)

        acroform = pdf.Root.AcroForm
        for key, val in acroform.items():
            print(f"Key: {key} (type: {type(key)}), Value: {val} (type: {type(val)})")

        fields = acroform['/Fields']
        for field in fields:
            field_name = field.get('/T')
            print(f"Field Name: {field_name}")
            mapping = get_mapping(case_data)
            value = mapping[field_name]
            if isinstance(value, str):            
                field.update(PdfDict(
                    V=PdfString.encode(value),
                    DV=PdfString.encode(value)
                ))
            elif isinstance(value, bool):
                if value:
                    if PdfName("On") in field.AP.N.keys():
                    # Common "On" value is usually "Yes", but you can inspect field['/AP']['/N'].keys() for actual value
                        on_value = PdfName("On")
                    elif PdfName("Yes") in field.AP.N.keys():
                        on_value = PdfName('Yes')
                    field.update(PdfDict(
                        V=on_value,
                        AS=on_value
                    ))

        case_number = case_data.case.summary.case_number
        PdfWriter().write(f"{temp_dir}/{case_number}.pdf", pdf)
        return f"{temp_dir}/{case_number}.pdf", f"{case_number}.pdf"
