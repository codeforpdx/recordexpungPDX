from dataclasses import dataclass
from io import BytesIO
from os import path

from dacite import from_dict
from flask.views import MethodView
from flask import request, json, make_response

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
    court: str
    da: str
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
    convicted_charges_1: str
    defendant_name: str


class FormFilling(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        record_summary = Search().build_response()
        charge = record_summary.record.cases[0].charges[0]
        form_data_dict = {
            **user_information,
            "court": charge.case_number,
            "da": "",
            "arresting_agency": "",
            "arrest_date": charge.date.strftime("%b %-d, %Y"),
            "conviction_date": "",
            "convicted_charges_1": "",
            "defendant_name": "Test",
        }
        form = from_dict(data_class=FormData, data=form_data_dict)
        from pathlib import Path

        pdf_path = path.join(Path(__file__).parent.parent, "files", "form.pdf")
        pdf = PdfReader(pdf_path)
        for field in pdf.Root.AcroForm.Fields:
            field_name = field.T.lower().replace(" ", "_").replace("(", "").replace(")", "")
            field_value = getattr(form, field_name)
            field.V = field_value
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
        # TODO: Write out to temp file
        # File name: NAME_CASE_{Convicted/Dismissed}.pdf
        # Create tar
        #
        # import tarfile
        # tar = tarfile.open("sample.tar", "w")
        # for name in ["foo", "bar", "quux"]:
        #     tar.add(name)
        # tar.close()
        data = FormFilling.to_bytes(pdf)
        response = make_response(data)
        response.headers["Content-Type"] = "application/pdf"
        filename = "test.pdf"
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        return response

    @staticmethod
    def to_bytes(pdf):
        output = BytesIO()
        PdfWriter().write(output, pdf)
        output.seek(0)
        return output.read()


def register(app):
    app.add_url_rule("/api/pdf", view_func=Pdf.as_view("pdf"))
    app.add_url_rule("/api/expungement-packet", view_func=FormFilling.as_view("expungement-packet"))
