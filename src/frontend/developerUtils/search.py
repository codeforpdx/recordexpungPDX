from flask.views import MethodView
from flask import request, current_app
from flask_login import login_required

from expungeservice.generator import build_record
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.record_summarizer import RecordSummarizer


class Search(MethodView):
    @login_required
    def post(self):
        request_data = request.get_json()

        if request_data is None or not request_data.get("names"):
            error(400, "No json data in request body")

        for alias in request_data["names"]:
            check_data_fields(alias, ["first_name", "last_name", "middle_name", "birth_date"])

        record = build_record()
        record_summary = RecordSummarizer.summarize(record)
        response_data = {"data": {"record": record_summary}}

        current_app.json_encoder = ExpungeModelEncoder

        return response_data  # Json-encoding happens automatically here


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
