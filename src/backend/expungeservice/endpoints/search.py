from dacite import from_dict
from flask.views import MethodView
from flask import request, current_app, json

from expungeservice.models.record import QuestionSummary, Alias
from expungeservice.record_creator import RecordCreator
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.util import LRUCache


class Search(MethodView):
    search_cache = LRUCache(4)

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
        record, questions = RecordCreator.build_record(
            RecordCreator.build_search_results, username, password, tuple(aliases), edits_data, Search.search_cache
        )
        if questions_data:
            questions = Search._build_questions(questions_data)
        record_summary = RecordSummarizer.summarize(record, questions)
        response_data = {"record": record_summary}
        return json.dumps(response_data, cls=ExpungeModelEncoder)

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
    def _validate_request(request_data):
        check_data_fields(request_data, ["aliases"])
        for alias in request_data["aliases"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
