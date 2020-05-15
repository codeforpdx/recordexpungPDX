from dacite import from_dict
from flask.views import MethodView
from flask import request, current_app, json, make_response
from flask_login import login_required
import logging

from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Question, Alias
from expungeservice.record_creator import RecordCreator
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.database.db_util import save_search_event


class Search(MethodView):
    @login_required
    def post(self):
        request_data = request.get_json()

        Search._validate_request(request_data)
        username, password = Search._oeci_login_params(request)

        return Search._build_response(
            username, password, request_data["aliases"], request_data.get("questions"), request_data.get("edits", {})
        )

    @staticmethod
    def _build_response(username, password, aliases_data, questions_data, edits_data):
        aliases = [from_dict(data_class=Alias, data=alias) for alias in aliases_data]
        record, ambiguous_record, questions, disposition_was_unknown = RecordCreator.build_record(
            RecordCreator.build_search_results, username, password, tuple(aliases), edits_data
        )
        if questions_data:
            questions, record = Search.disambiguate_record(ambiguous_record, questions_data)
        try:
            save_search_event(aliases_data)
        except Exception as ex:
            logging.error("Saving search result failed with exception: %s" % ex, stack_info=True)
        record_summary = RecordSummarizer.summarize(record, questions, disposition_was_unknown)
        response_data = {"record": record_summary}
        return json.dumps(response_data, cls=ExpungeModelEncoder)

    @staticmethod
    def disambiguate_record(ambiguous_record, questions_data):
        questions_as_list = [from_dict(data_class=Question, data=question) for id, question in questions_data.items()]
        questions = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions_as_list)))
        updated_ambiguous_record = RecordMerger.filter_ambiguous_record(ambiguous_record, questions_as_list)
        record = RecordCreator.analyze_ambiguous_record(updated_ambiguous_record)
        return questions, record

    @staticmethod
    def _oeci_login_params(request):
        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))
        if not "oeci_token" in request.cookies.keys():
            error(401, "Missing login credentials to OECI.")
        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])
        return decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"]

    @staticmethod
    def _validate_request(request_data):
        check_data_fields(request_data, ["aliases"])
        for alias in request_data["aliases"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])


class Print(MethodView):
    @login_required
    def post(self):
        response = Search.post(self)
        record = json.loads(response)["record"]
        request_data = request.get_json()
        aliases = request_data["aliases"]
        filename = Print.build_filename(aliases)
        header = MarkdownSerializer.default_header(aliases)
        source = MarkdownSerializer.to_markdown(record, header)
        pdf = MarkdownToPDF.to_pdf("Expungement analysis", source)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        return response

    @staticmethod
    def build_filename(aliases):
        first_alias = aliases[0]
        name = f"{first_alias['first_name']}_{first_alias['last_name']}".upper()
        return f"{name}_record_summary.pdf"


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
    app.add_url_rule("/api/pdf", view_func=Print.as_view("pdf"))
