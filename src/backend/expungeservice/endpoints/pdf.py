from dataclasses import dataclass
from os import path
from pathlib import Path
from tempfile import mkdtemp
from zipfile import ZipFile

from dacite import from_dict
from expungeservice.expunger import Expunger
from expungeservice.models.expungement_result import ChargeEligibilityStatus
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

    arrest_dates_all: str
    charges_all: str

    dismissed_charges: str
    dismissed_arrest_dates: str
    dismissed_dates: str

    conviction_charges: str
    conviction_arrest_dates: str
    conviction_dates: str

    defendant_name: str
    county: str


class FormFilling(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        record_summary = Search().build_response()
        temp_dir = mkdtemp()
        zip_dir = mkdtemp()
        zip_name = "expungement_packet.zip"
        zip_path = path.join(zip_dir, zip_name)
        zipfile = ZipFile(zip_path, "w")
        for case in record_summary.record.cases:
            pdf = FormFilling._build_pdf_for_case(case, user_information)
            if pdf:
                file_name = f"{case.summary.name}_{case.summary.case_number}.pdf"
                file_path = path.join(temp_dir, file_name)
                PdfWriter().write(file_path, pdf)
                zipfile.write(file_path, file_name)
        zipfile.close()
        return send_file(zip_path, as_attachment=True, attachment_filename=zip_name)

    @staticmethod
    def _build_pdf_for_case(case, user_information):
        eligible_charges = [
            charge
            for charge in case.charges
            if charge.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
        ]
        if eligible_charges:
            return FormFilling._build_pdf_for_eligible_case(case, eligible_charges, user_information)

    @staticmethod
    def _build_pdf_for_eligible_case(case, eligible_charges, user_information):
        dismissals, convictions = Expunger._categorize_charges(eligible_charges)
        dismissed_names = [charge.name for charge in dismissals]
        dismissed_arrest_dates = list(set([charge.date.strftime("%b %-d, %Y") for charge in dismissals]))
        dismissed_dates = list(set([charge.disposition.date.strftime("%b %-d, %Y") for charge in dismissals]))
        conviction_names = [charge.name for charge in convictions]
        conviction_arrest_dates = list(set([charge.date.strftime("%b %-d, %Y") for charge in convictions]))
        conviction_dates = list(set([charge.disposition.date.strftime("%b %-d, %Y") for charge in convictions]))
        arrest_dates_all = list(set(dismissed_arrest_dates + conviction_arrest_dates))
        charge_names = dismissed_names + conviction_names
        form_data_dict = {
            **user_information,
            "case_name": case.summary.name,
            "case_number": case.summary.case_number,
            "da_number": "N/A",
            "arresting_agency": "N/A",
            "arrest_dates_all": "; ".join(arrest_dates_all),
            "charges_all": "; ".join(charge_names),
            "dismissed_charges": "; ".join(dismissed_names),
            "dismissed_arrest_dates": "; ".join(dismissed_arrest_dates),
            "dismissed_dates": "; ".join(dismissed_dates),
            "conviction_charges": "; ".join(conviction_names),
            "conviction_arrest_dates": "; ".join(conviction_arrest_dates),
            "conviction_dates": "; ".join(conviction_dates),
            "defendant_name": case.summary.name,
            "county": case.summary.location,
        }
        form = from_dict(data_class=FormData, data=form_data_dict)
        pdf_path = FormFilling.build_pdf_path(case, convictions)
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
    def build_pdf_path(case, convictions):
        if convictions:
            if case.summary.location.lower() == "multnomah":
                return path.join(Path(__file__).parent.parent, "files", f"multnomah_conviction.pdf")
            else:
                return path.join(Path(__file__).parent.parent, "files", f"stock_conviction.pdf")
        else:
            if case.summary.location.lower() == "multnomah":
                return path.join(Path(__file__).parent.parent, "files", f"multnomah_arrest.pdf")
            else:
                return path.join(Path(__file__).parent.parent, "files", f"stock_arrest.pdf")


def register(app):
    app.add_url_rule("/api/pdf", view_func=Pdf.as_view("pdf"))
    app.add_url_rule("/api/expungement-packet", view_func=FormFilling.as_view("expungement-packet"))
