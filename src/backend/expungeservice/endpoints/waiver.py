from expungeservice.endpoints.demo import Demo
from expungeservice.form_filling import FormFilling
from flask.views import MethodView
from flask import request, json, make_response, send_file

from expungeservice.pdf.markdown_renderer import MarkdownRenderer
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF
from expungeservice.endpoints.search import Search


class WaiverPDF(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        waiver_information = request_data.get("waiverInformation")
        demo = request_data.get("demo")
        search = Demo if demo else Search
        record_summary = search().build_response()  # type: ignore
        response = search().post()  # type: ignore
        record = json.loads(response)["record"]
        aliases = request_data["aliases"]
        source = MarkdownRenderer.to_markdown(record, aliases=aliases)
        summary_pdf_bytes = MarkdownToPDF.to_pdf("Expungement analysis", source)
        summary_filename = FormFilling.build_summary_filename(aliases)
        zip_path, zip_name = FormFilling.build_zip(record_summary, user_information, summary_pdf_bytes, summary_filename)
        print("waiver info:", waiver_information)
        return send_file(zip_path, as_attachment=True, attachment_filename=zip_name)

    @staticmethod
    def build_summary_filename(aliases):
        first_alias = aliases[0]
        name = f"{first_alias['first_name']}_{first_alias['last_name']}".upper()
        return f"{name}_record_summary.pdf"


def register(app):
    app.add_url_rule("/api/waiver-packet", view_func=WaiverPDF.as_view("waiver-packet"))
