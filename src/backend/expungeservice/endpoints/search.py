import pickle
from typing import List, Any, Dict

from dacite import from_dict
from flask.views import MethodView
from flask import request, current_app, session, json
from flask_login import login_required
import logging

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Question
from expungeservice.record_creator import RecordCreator
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.stats import save_result
from expungeservice.record_summarizer import RecordSummarizer


class Search(MethodView):
    @login_required
    def post(self):
        request_data = request.get_json()
        if request_data is None or not request_data.get("aliases"):
            error(400, "No json data in request body")
        check_data_fields(request_data, ["aliases"])
        for alias in request_data["aliases"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])

        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))

        if not "oeci_token" in request.cookies.keys():
            error(401, "Missing login credentials to OECI.")
        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])
        username, password = decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"]

        record, ambiguous_record, questions = RecordCreator.build_record(username, password, request_data["aliases"])
        if questions:
            session["ambiguous_record"] = pickle.dumps(ambiguous_record)

        try:
            save_result(request_data, record)
        except Exception as ex:
            logging.error("Saving search result failed with exception: %s" % ex, stack_info=True)

        record_summary = RecordSummarizer.summarize(record, questions)
        response_data = {"data": {"record": record_summary}}
        encoded_response = json.dumps(response_data, cls=ExpungeModelEncoder)
        return encoded_response


class Disambiguate(MethodView):
    @login_required
    def post(self):
        ambiguous_record_data = session.get("ambiguous_record")
        if ambiguous_record_data:
            ambiguous_record = pickle.loads(ambiguous_record_data)
            request_data = request.get_json()
            questions = request_data.get("questions")
            return Disambiguate.build_response(ambiguous_record, questions)
        else:
            error(428, "Must hit the search endpoint with question generating records first.")

    @staticmethod
    def build_response(ambiguous_record: AmbiguousRecord, questions_data: Dict[str, Any]):
        questions = [from_dict(data_class=Question, data=question) for id, question in questions_data.items()]
        questions_as_dict = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions)))
        updated_ambiguous_record = RecordMerger.filter_ambiguous_record(ambiguous_record, questions)
        record = RecordCreator.analyze_ambiguous_record(updated_ambiguous_record)
        record_summary = RecordSummarizer.summarize(record, questions_as_dict)
        response_data = {"data": {"record": record_summary}}
        return json.dumps(response_data, cls=ExpungeModelEncoder)


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
    app.add_url_rule("/api/disambiguate", view_func=Disambiguate.as_view("disambiguate"))
