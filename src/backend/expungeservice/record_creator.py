from itertools import product, groupby
from typing import List, Dict

from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCase, AmbiguousRecord
from expungeservice.models.helpers.record_merger import RecordMerger
from expungeservice.models.record import Record
from expungeservice.request import error


class RecordCreator:
    @staticmethod
    def build_record(username: str, password: str, aliases: List[Dict[str, str]]) -> Record:
        ambiguous_cases: List[AmbiguousCase] = []
        errors = []
        for alias in aliases:
            crawler = Crawler()
            login_result = crawler.login(username, password, close_session=False)
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
                record.errors += ErrorChecker.check(record)  # TODO: Fix mutation
                expunger = Expunger(record)
                charge_id_to_time_eligibility = expunger.run()
                charge_id_to_time_eligibilities.append(charge_id_to_time_eligibility)
            record = RecordMerger.merge(ambiguous_record, charge_id_to_time_eligibilities)
        return record
