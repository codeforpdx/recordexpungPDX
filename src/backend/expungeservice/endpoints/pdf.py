from dataclasses import dataclass
from io import BytesIO
from os import path
from pathlib import Path
from tempfile import mkdtemp
import tarfile

from dacite import from_dict
from expungeservice.expunger import Expunger
from flask.views import MethodView
from flask import request, json, make_response, send_file

from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF
from expungeservice.endpoints.search import Search
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject


class Pdf(MethodView):
    def post(self):
        response = Search().post()
        record = json.loads(response)["record"]
        request_data = request.get_json()
        aliases = request_data["aliases"]
        header = MarkdownSerializer.default_header(aliases)
        source = MarkdownSerializer.to_markdown(record, header)
        pdf = MarkdownToPDF.to_pdf("Expungement analysis", source)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        filename = Pdf.build_filename(aliases)
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        return response

    @staticmethod
    def build_filename(aliases):
        first_alias = aliases[0]
        name = f"{first_alias['first_name']}_{first_alias['last_name']}".upper()
        return f"{name}_record_summary.pdf"


@dataclass
class FormData:
    case_name: str
    case_number: str
    da_number: str
    full_name: str
    date_of_birth: str
    mailing_address: str
    phone_number: str
    city: str
    state: str
    zip_code: str
    arresting_agency: str
    arrest_date: str
    conviction_date: str
    disposition_date: str  # This is for acquittals
    convicted_charges: str
    defendant_name: str


class FormFilling(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        record_summary = Search().build_response()
        temp_dir = mkdtemp()
        tar_dir = mkdtemp()
        tar_name = "expungement_packet.tar"
        tar_path = path.join(tar_dir, tar_name)
        tar = tarfile.open(tar_path, "w")
        for case in record_summary.record.cases:
            pdf = FormFilling.build_pdf_for_case(case, user_information)
            file_name = f"{case.summary.name}_{case.summary.case_number}.pdf"
            file_path = path.join(temp_dir, file_name)
            PdfWriter().write(file_path, pdf)
            tar.add(file_path)
        tar.close()
        return send_file(tar_path, as_attachment=True, attachment_filename=tar_name)

    @staticmethod
    def build_pdf_for_case(case, user_information):
        county = "clackamas"  # TODO: Swap with case.location
        dismissals, convictions = Expunger._categorize_charges(case.charges)
        arrest_dates = [conviction.date.strftime("%b %-d, %Y") for conviction in convictions]
        conviction_dates = [conviction.disposition.date.strftime("%b %-d, %Y") for conviction in convictions]
        conviction_names = [conviction.name for conviction in convictions]
        form_data_dict = {
            **user_information,
            "case_name": case.summary.name,
            "case_number": case.summary.case_number,
            "da_number": "N/A",
            "arresting_agency": "N/A",
            "arrest_date": ";".join(arrest_dates),
            "conviction_date": ";".join(conviction_dates),
            "convicted_charges": ";".join(conviction_names),
            "disposition_date": "N/A",
            "defendant_name": case.summary.name,
        }
        form = from_dict(data_class=FormData, data=form_data_dict)
        pdf_path = path.join(Path(__file__).parent.parent, "files", f"{county}_arrest.pdf")
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
    def to_bytes(pdf):
        output = BytesIO()
        PdfWriter().write(output, pdf)
        output.seek(0)
        return output.read()


def register(app):
    app.add_url_rule("/api/pdf", view_func=Pdf.as_view("pdf"))
    app.add_url_rule("/api/expungement-packet", view_func=FormFilling.as_view("expungement-packet"))
