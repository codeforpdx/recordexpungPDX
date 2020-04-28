from dataclasses import replace
from functools import lru_cache
from itertools import product, groupby
from typing import List, Dict, Tuple

import requests

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase, AmbiguousRecord
from expungeservice.models.case import Case, OeciCase
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Question, Alias
from expungeservice.request import error


class RecordCreator:
    @staticmethod
    @lru_cache(maxsize=4)
    def build_record(
        username: str, password: str, aliases: Tuple[Alias, ...]
    ) -> Tuple[Record, AmbiguousRecord, Dict[str, Question]]:
        search_results, errors = RecordCreator._build_search_results(username, password, aliases)
        if errors:
            record = Record((), tuple(errors))
            ambiguous_record = [record]
            return record, ambiguous_record, {}
        else:
            cases_with_unique_case_number: List[OeciCase] = [
                list(group)[0]
                for key, group in groupby(
                    sorted(search_results, key=lambda case: case.summary.case_number),
                    lambda case: case.summary.case_number,
                )
            ]
            user_edited_search_results = RecordCreator.edit_search_results(
                cases_with_unique_case_number, user_edits=None
            )
            ambiguous_record, questions = RecordCreator.build_ambiguous_record(user_edited_search_results)
            record = RecordCreator.analyze_ambiguous_record(ambiguous_record)
            questions_as_dict = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions)))
            return record, ambiguous_record, questions_as_dict

    # TODO: In the future we will add a cache here
    @staticmethod
    def _build_search_results(
        username: str, password: str, aliases: Tuple[Alias, ...]
    ) -> Tuple[List[OeciCase], List[str]]:
        errors = []
        search_results: List[OeciCase] = []
        for alias in aliases:
            session = requests.Session()
            try:
                login_response = Crawler.attempt_login(session, username, password)
                alias_search_result = Crawler.search(
                    session, login_response, alias.first_name, alias.last_name, alias.middle_name, alias.birth_date,
                )
                search_results += alias_search_result
            except InvalidOECIUsernamePassword as e:
                error(401, str(e))
            except OECIUnavailable as e:
                error(404, str(e))
            except Exception as e:
                errors.append(str(e))
            finally:
                session.close()
        return search_results, errors

    @staticmethod
    def build_ambiguous_record(search_result: List[OeciCase]) -> Tuple[AmbiguousRecord, List[Question]]:
        ambiguous_record: AmbiguousRecord = []
        questions_accumulator: List[Question] = []
        ambiguous_cases: List[AmbiguousCase] = []
        for oeci_case in search_result:
            ambiguous_case, questions = RecordCreator._build_case(oeci_case)
            questions_accumulator += questions
            ambiguous_cases.append(ambiguous_case)
        for cases in product(*ambiguous_cases):
            ambiguous_record.append(Record(tuple(cases)))
        return ambiguous_record, questions_accumulator

    @staticmethod
    def analyze_ambiguous_record(ambiguous_record: AmbiguousRecord):
        charge_id_to_time_eligibilities = []
        ambiguous_record_with_errors = []
        for record in ambiguous_record:
            record_with_errors = replace(record, errors=tuple(ErrorChecker.check(record)))
            charge_id_to_time_eligibility = Expunger.run(record_with_errors)
            charge_id_to_time_eligibilities.append(charge_id_to_time_eligibility)
            ambiguous_record_with_errors.append(record_with_errors)
        record = RecordMerger.merge(ambiguous_record_with_errors, charge_id_to_time_eligibilities)
        sorted_record = RecordCreator.sort_record_by_case_date(record)
        return sorted_record

    @staticmethod
    def sort_record_by_case_date(record):
        sorted_cases = sorted(record.cases, key=lambda case: case.summary.date, reverse=True)
        return replace(record, cases=tuple(sorted_cases))

    @staticmethod
    def _build_case(oeci_case: OeciCase) -> Tuple[AmbiguousCase, List[Question]]:
        ambiguous_charges: List[AmbiguousCharge] = []
        questions: List[Question] = []
        for oeci_charge in oeci_case.charges:
            charge_id = oeci_charge.id
            charge_dict = {
                "name": oeci_charge.name,
                "statute": oeci_charge.statute,
                "level": oeci_charge.level,
                "date": oeci_charge.date,
                "disposition": oeci_charge.disposition,
                "case_number": oeci_case.summary.case_number,
                "violation_type": oeci_case.summary.violation_type,
                "birth_year": oeci_case.summary.birth_year,
            }
            ambiguous_charge, question = ChargeCreator.create(charge_id, **charge_dict)
            ambiguous_charges.append(ambiguous_charge)
            if question:
                questions.append(question)
        ambiguous_case: AmbiguousCase = []
        for charges in product(*ambiguous_charges):
            possible_case = Case(oeci_case.summary, charges=tuple(charges))
            ambiguous_case.append(possible_case)
        return ambiguous_case, questions

    # TODO: implement.
    @staticmethod
    def edit_search_results(cases_with_unique_case_number: List[OeciCase], user_edits) -> List[OeciCase]:
        return cases_with_unique_case_number
