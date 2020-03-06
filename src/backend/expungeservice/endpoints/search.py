from itertools import groupby, product
from typing import List

from flask.views import MethodView
from flask import request, current_app
from flask_login import login_required
import logging

from expungeservice.models.helpers.record_merger import RecordMerger
from expungeservice.models.record import Record
from expungeservice.models.ambiguous import AmbiguousCase, AmbiguousRecord
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger import Expunger, ErrorChecker
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
from expungeservice.stats import save_result
from expungeservice.models.helpers.record_summarizer import RecordSummarizer


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

        ambiguous_cases: List[AmbiguousCase] = []
        errors = []
        for alias in request_data["aliases"]:
            crawler = Crawler()
            login_result = crawler.login(
                decrypted_credentials["oeci_username"], decrypted_credentials["oeci_password"], close_session=False
            )
            if login_result is False:
                error(401, "Attempted login to OECI failed")

            try:
                ambiguous_cases += crawler.search(
                    alias["first_name"], alias["last_name"], alias["middle_name"], alias["birth_date"],
                )

            except Exception as e:
                errors.append(str(e))

        if errors:
            record = Record([], errors)
        else:
            ambiguous_record: AmbiguousRecord = []
            for cases in product(*ambiguous_cases):
                cases_with_unique_case_number = [
                    list(group)[0]
                    for key, group in groupby(
                        sorted(list(cases), key=lambda case: case.case_number), lambda case: case.case_number
                    )
                ]
                ambiguous_record.append(Record(cases_with_unique_case_number))

            charge_id_to_time_eligibilities = []
            for record in ambiguous_record:
                record.errors += ErrorChecker.check(record)
                expunger = Expunger(record)
                charge_id_to_time_eligibility = expunger.run()
                charge_id_to_time_eligibilities.append(charge_id_to_time_eligibility)
            record = RecordMerger.merge(ambiguous_record, charge_id_to_time_eligibilities)

        try:
            save_result(request_data, record)
        except Exception as ex:
            logging.error("Saving search result failed with exception: %s" % ex, stack_info=True)

        record_summary = RecordSummarizer.summarize(record)
        response_data = {"data": {"record": record_summary}}

        current_app.json_encoder = ExpungeModelEncoder

        return response_data  # Json-encoding happens automatically here


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
