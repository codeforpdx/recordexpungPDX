from dacite import from_dict
from flask.views import MethodView
from flask import request
import json

from expungeservice.models.record import Alias
from expungeservice.record_creator import RecordCreator
from expungeservice.demo_records import DemoRecords
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.util import LRUCache
from expungeservice.endpoints.search import Search


class Demo(MethodView):
    search_cache = LRUCache(4)

    def post(self):
        record_summary = self.build_response()
        response_data = {"record": record_summary}
        return json.dumps(response_data, cls=ExpungeModelEncoder)

    def build_response(self):
        request_data = request.get_json()
        Search._validate_request(request_data)
        today = Search._build_today(request_data.get("today", ""))
        return Demo._build_record_summary(
            request_data["aliases"], request_data.get("questions"), request_data.get("edits", {}), today
        )

    @staticmethod
    def _build_record_summary(aliases_data, questions_data, edits_data, today):
        aliases = [from_dict(data_class=Alias, data=alias) for alias in aliases_data]
        record, questions = RecordCreator.build_record(
            DemoRecords.build_search_results,
            "username",
            "password",
            tuple(aliases),
            edits_data,
            today,
            Demo.search_cache,
        )
        if questions_data:
            questions = Search._build_questions(questions_data)
        return RecordSummarizer.summarize(record, questions)


def register(app):
    app.add_url_rule("/api/demo", view_func=Demo.as_view("demo"))
