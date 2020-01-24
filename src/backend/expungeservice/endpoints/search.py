from flask.views import MethodView
from flask import request, current_app
from flask_login import login_required
import logging

from expungeservice.request import check_data_fields
from expungeservice.request.error import error
from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger.expunger import Expunger
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.stats import save_result
from expungeservice.models.helpers.record_summarizer import RecordSummarizer


class Search(MethodView):
    @login_required
    def post(self):
        request_data = request.get_json()

        if request_data is None:
            error(400, "No json data in request body")

        check_data_fields(request_data, ["first_name", "last_name", "middle_name", "birth_date"])

        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))

        if not "oeci_token" in request.cookies.keys():
            error(401, "Missing login credentials to OECI.")

        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])

        crawler = Crawler()

        login_result = crawler.login(
            decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"], close_session=False
        )

        if login_result is False:
            error(401, "Attempted login to OECI failed")

        record = crawler.search(
            request_data["first_name"],
            request_data["last_name"],
            request_data["middle_name"],
            request_data["birth_date"],
        )

        expunger = Expunger(record)
        expunger.run()

        try:
            save_result(request_data, record)
        except Exception as ex:
            logging.error("Saving search result failed with exception: %s" % ex, stack_info=True)

        record.summary = RecordSummarizer.summarize(record)
        response_data = {"data": {"record": record}}

        current_app.json_encoder = ExpungeModelEncoder

        return response_data  # Json-encoding happens automatically here

def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
