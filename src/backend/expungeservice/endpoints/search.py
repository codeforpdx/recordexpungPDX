from datetime import datetime
from dacite import from_dict
from expungeservice.models.record_summary import RecordSummary
from flask.views import MethodView
from flask import request, current_app
import json

from expungeservice.models.record import QuestionSummary, Alias
from expungeservice.record_creator import RecordCreator
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.util import LRUCache, DateWithFuture as date_class


class Search(MethodView):
    search_cache = LRUCache(4)

    def post(self):
        record_summary = self.build_response()
        response_data = {"record": record_summary}
        return json.dumps(response_data, cls=ExpungeModelEncoder, sort_keys=False)

    def build_response(self) -> RecordSummary:
        request_data = request.get_json()
        Search._validate_request(request_data)
        username, password = Search._oeci_login_params(request)
        today = Search._build_today(request_data.get("today", ""))
        return Search._build_record_summary(
            username,
            password,
            request_data["aliases"],
            request_data.get("questions"),
            request_data.get("edits", {}),
            today,
        )

    @staticmethod
    def _build_record_summary(username, password, aliases_data, questions_data, edits_data, today) -> RecordSummary:
        aliases = [from_dict(data_class=Alias, data=alias) for alias in aliases_data]
        record, questions = RecordCreator.build_record(
            RecordCreator.build_search_results,
            username,
            password,
            tuple(aliases),
            edits_data,
            today,
            Search.search_cache,
        )
        if questions_data:
            questions = Search._build_questions(questions_data)
        return RecordSummarizer.summarize(record, questions)

    @staticmethod
    def _build_questions(questions_data):
        questions_as_list = [
            from_dict(data_class=QuestionSummary, data=question) for id, question in questions_data.items()
        ]
        return dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions_as_list)))

    @staticmethod
    def _oeci_login_params(request):
        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))
        if not "oeci_token" in request.cookies.keys():
            error(401, "Missing login credentials to OECI.")
        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])
        return decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"]

    @staticmethod
    def _build_today(today_string: str) -> date_class:
        try:
            today_datetime = datetime.strptime(today_string, "%m/%d/%Y")
            return date_class.fromdatetime(today_datetime)
        except:
            return date_class.today()

    @staticmethod
    def _validate_request(request_data):
        check_data_fields(request_data, ["aliases"])
        for alias in request_data["aliases"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
