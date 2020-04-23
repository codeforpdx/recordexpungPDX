from dacite import from_dict
from flask.views import MethodView
from flask import request, current_app, json
from flask_login import login_required
import logging

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
        if request_data is None or not request_data.get("aliases"):
            error(400, "No json data in request body")
        check_data_fields(request_data, ["aliases"])
        for alias in request_data["aliases"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])
        aliases_data = request_data["aliases"]
        questions_data = request_data.get("questions")
        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))
        if not "oeci_token" in request.cookies.keys():
            error(401, "Missing login credentials to OECI.")
        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])
        username, password = decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"]
        return Search.build_response(username, password, aliases_data, questions_data)

    @staticmethod
    def build_response(username, password, aliases_data, questions_data):
        aliases = [from_dict(data_class=Alias, data=alias) for alias in aliases_data]
        record, ambiguous_record, questions = RecordCreator.build_record(username, password, tuple(aliases))
        if questions_data:
            questions, record = Search.disambiguate_record(ambiguous_record, questions_data)
        try:
            save_search_event(aliases_data)
        except Exception as ex:
            logging.error("Saving search result failed with exception: %s" % ex, stack_info=True)
        record_summary = RecordSummarizer.summarize(record, questions)
        response_data = {"record": record_summary}
        return json.dumps(response_data, cls=ExpungeModelEncoder)

    @staticmethod
    def disambiguate_record(ambiguous_record, questions_data):
        questions_as_list = [from_dict(data_class=Question, data=question) for id, question in questions_data.items()]
        questions = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions_as_list)))
        updated_ambiguous_record = RecordMerger.filter_ambiguous_record(ambiguous_record, questions_as_list)
        record = RecordCreator.analyze_ambiguous_record(updated_ambiguous_record)
        return questions, record


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
