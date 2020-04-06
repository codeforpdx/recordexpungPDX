from itertools import product, groupby
from typing import List, Dict, Tuple
from dataclasses import replace

from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCase, AmbiguousRecord
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Question
from expungeservice.request import error


class RecordCreator:
    @staticmethod
    def build_record(
        username: str, password: str, aliases: List[Dict[str, str]]
    ) -> Tuple[Record, AmbiguousRecord, List[Question]]:
        ambiguous_cases_accumulator: List[AmbiguousCase] = []
        questions_accumulator: List[Question] = []
        errors = []
        for alias in aliases:
            crawler = Crawler()
            login_result = crawler.login(username, password, close_session=False)
            if login_result is False:
                error(401, "Attempted login to OECI failed")

            try:
                search_result = crawler.search(
                    alias["first_name"], alias["last_name"], alias["middle_name"], alias["birth_date"],
                )
                ambiguous_cases, questions = search_result
                ambiguous_cases_accumulator += ambiguous_cases
                questions_accumulator += questions
            except Exception as e:
                errors.append(str(e))
        if errors:
            ambiguous_record = [Record([], errors)]
        else:
            ambiguous_record: AmbiguousRecord = []  # type: ignore
            for cases in product(*ambiguous_cases_accumulator):
                cases_with_unique_case_number = [
                    list(group)[0]
                    for key, group in groupby(
                        sorted(list(cases), key=lambda case: case.case_number), lambda case: case.case_number
                    )
                ]
                ambiguous_record.append(Record(cases_with_unique_case_number))
        record = RecordCreator.analyze_ambiguous_record(ambiguous_record)
        return record, ambiguous_record, questions_accumulator
        
    @staticmethod
    def analyze_ambiguous_record(ambiguous_record: AmbiguousRecord):
        charge_id_to_time_eligibilities = []
        for record in ambiguous_record:
            record.errors += ErrorChecker.check(record)  # TODO: Fix mutation
            expunger = Expunger(record)
            charge_id_to_time_eligibility = expunger.run()
            charge_id_to_time_eligibilities.append(charge_id_to_time_eligibility)
        record = RecordMerger.merge(ambiguous_record, charge_id_to_time_eligibilities)
        return record
        
        
    @staticmethod
    def sort_record_by_case_date(record):
        sortedCases = sorted(record.cases, key = lambda case: case.date, reverse = True)
        return replace(record, cases=sortedCases)
        