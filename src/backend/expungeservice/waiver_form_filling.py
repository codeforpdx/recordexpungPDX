from dataclasses import dataclass
from tempfile import mkdtemp
from os import path
from pathlib import Path
from typing import Dict, Tuple
from pdfrw import PdfReader, PdfDict, PdfString, PdfWriter, PdfName, PdfObject
from zipfile import ZipFile
from datetime import date
import re

from expungeservice.models.record_summary import RecordSummary
from expungeservice.models.case import Case
from expungeservice.form_filling import DA_ADDRESSES, FormFilling

def wrap_text(text):
    text = re.sub(r'\r\n?|\n', ' ', text)
    lines = []
    while text:
        if len(text) <= 90:
            lines.append(text)
            break
        split_index = text.find(' ', 90)
        if split_index == -1:
            lines.append(text)
            break
        lines.append(text[:split_index])
        text = text[split_index+1:]
    return lines[:4]

@dataclass
class CaseData:
    case: Case
    user_information_dict: Dict
    waiver_information_dict: Dict


def get_mapping(case_data: CaseData):
    benefit = case_data.waiver_information_dict["snap"] or case_data.waiver_information_dict["ssi"] or case_data.waiver_information_dict["tanf"] or case_data.waiver_information_dict["ohp"]
    today = date.today().strftime("%b %-d, %Y")
    da_address_lines = DA_ADDRESSES[case_data.case.summary.location.lower()].split("-")
    explain_lines = wrap_text(case_data.waiver_information_dict["explain"])
    ask_lines = wrap_text(case_data.waiver_information_dict["explain2"])
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
        "(Explain1)": explain_lines[0] if len(explain_lines) > 0 else "",
        "(Explain2)": explain_lines[1] if len(explain_lines) > 1 else "",
        "(Explain3)": explain_lines[2] if len(explain_lines) > 2 else "",
        "(Explain4)": explain_lines[3] if len(explain_lines) > 3 else "",
        "(Ask1)": ask_lines[0] if len(ask_lines) > 0 else "",
        "(Ask2)": ask_lines[1] if len(ask_lines) > 1 else "",
        "(Ask3)": ask_lines[2] if len(ask_lines) > 2 else "",
        "(Ask4)": ask_lines[3] if len(ask_lines) > 3 else "",
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

        all_waiver_files = []
        for case in record_summary.record.cases:
            if (
                case.summary.balance_due_in_cents > 0
                and case.summary.location.lower() not in WaiverFormFilling.COUNTIES_WITHOUT_WAIVER_PROGRAM
            ):
                case_data = CaseData(case, user_information_dict, waiver_information_dict)
                file_info = WaiverFormFilling._create_and_write_pdf(case_data, temp_dir)
                zip_file.write(*file_info[0:2])
                all_waiver_files.append(file_info)

        if all_waiver_files:
            file_paths = [f[0] for f in all_waiver_files]
            comp_path = path.join(temp_dir, "COMPILED_FINES_AND_FEES.pdf")
            FormFilling.compile_pdfs(file_paths, comp_path)
            zip_file.write(comp_path, "COMPILED_FINES_AND_FEES.pdf")

        zip_file.close()

        return zip_path, zip_file_name

    @staticmethod
    def _create_and_write_pdf(case_data: CaseData, temp_dir: str):
        file_name = "fee_waiver.pdf"
        source_dir = path.join(Path(__file__).parent, "files")
        pdf_path = path.join(source_dir, file_name)
        pdf = PdfReader(pdf_path)

        acroform = pdf.Root.AcroForm
        acroform.update(
        PdfDict(NeedAppearances=PdfObject('true'))
    )
        #for key, val in acroform.items():
        #    print(f"Key: {key} (type: {type(key)}), Value: {val} (type: {type(val)})")

        fields = acroform['/Fields']
        for field in fields:
            field_name = field.get('/T')
            mapping = get_mapping(case_data)
            value = mapping[field_name]
            if isinstance(value, str):
                field.update(PdfDict(
                    V=PdfString.encode(value),
                    DV=PdfString.encode(value)
                ))
                field.update(PdfDict(AP=""))

            elif isinstance(value, bool):
                if value:
                    if PdfName("On") in field.AP.N.keys():
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
