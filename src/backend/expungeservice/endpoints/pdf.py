from expungeservice.endpoints.demo import Demo
from expungeservice.form_filling import FormFilling
from flask.views import MethodView
from flask import request, make_response, send_file
import json

from expungeservice.pdf.markdown_renderer import MarkdownRenderer
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF
from expungeservice.endpoints.search import Search


class Pdf(MethodView):
    def post(self):
        request_data = request.get_json()
        demo = request_data.get("demo")
        search = Demo if demo else Search
        response = search().post()  # type: ignore
        record = json.loads(response)["record"]
        aliases = request_data["aliases"]
        source = MarkdownRenderer.to_markdown(record, aliases=aliases)
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


class FormPDF(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        demo = request_data.get("demo")
        search = Demo if demo else Search
        record_summary = search().build_response()  # type: ignore
        zip_path, zip_name = FormFilling.build_zip(record_summary, user_information)
        return send_file(zip_path, as_attachment=True, attachment_filename=zip_name)


def register(app):
    app.add_url_rule("/api/pdf", view_func=Pdf.as_view("pdf"))
    app.add_url_rule("/api/expungement-packet", view_func=FormPDF.as_view("expungement-packet"))
