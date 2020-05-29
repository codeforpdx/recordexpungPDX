from dataclasses import replace
from functools import lru_cache
from itertools import product, groupby
from typing import List, Dict, Tuple, Any, Callable

import requests

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase, AmbiguousRecord
from expungeservice.models.case import Case, OeciCase
from expungeservice.models.charge import Charge
from expungeservice.record_editor import RecordEditor
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Question, Alias
from expungeservice.request import error
from expungeservice.models.disposition import DispositionStatus


class RecordCreator:
    @staticmethod
    def build_record(
        search: Callable, username: str, password: str, aliases: Tuple[Alias, ...], edits: Dict[str, Dict[str, Any]],
    ) -> Tuple[Record, AmbiguousRecord, Dict[str, Question], List[str]]:
        search_results, errors = search(username, password, aliases)
        if errors:
            record = Record((), tuple(errors))
            ambiguous_record = [record]
            return record, ambiguous_record, {}, []
        else:
            cases_with_unique_case_number: List[OeciCase] = [
                list(group)[0]
                for key, group in groupby(
                    sorted(search_results, key=lambda case: case.summary.case_number),
                    lambda case: case.summary.case_number,
                )
            ]
            unknown_dispositions = RecordCreator._find_unknown_dispositions(cases_with_unique_case_number)
            user_edited_search_results, new_charges = RecordEditor.edit_search_results(
                cases_with_unique_case_number, edits
            )
            ambiguous_record, questions = RecordCreator.build_ambiguous_record(user_edited_search_results, new_charges)
            record = RecordCreator.analyze_ambiguous_record(ambiguous_record)
            updated_unknown_dispositions = RecordCreator._filter_for_blocking_charges(
                record.cases, unknown_dispositions
            )
            questions_as_dict = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions)))
            return record, ambiguous_record, questions_as_dict, updated_unknown_dispositions

    @staticmethod
    @lru_cache(maxsize=4)
    def build_search_results(
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
    def build_ambiguous_record(
        search_result: List[OeciCase], new_charges: List[Charge]
    ) -> Tuple[AmbiguousRecord, List[Question]]:
        ambiguous_record: AmbiguousRecord = []
        questions_accumulator: List[Question] = []
        ambiguous_cases: List[AmbiguousCase] = []
        for oeci_case in search_result:
            new_charges_in_case = list(
                filter(lambda charge: charge.case_number == oeci_case.summary.case_number, new_charges)
            )
            ambiguous_case, questions = RecordCreator._build_case(oeci_case, new_charges_in_case)
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
    def _build_case(oeci_case: OeciCase, new_charges: List[Charge]) -> Tuple[AmbiguousCase, List[Question]]:
        ambiguous_charges: List[AmbiguousCharge] = []
        questions: List[Question] = []
        for oeci_charge in oeci_case.charges:
            ambiguous_charge_id = oeci_charge.ambiguous_charge_id
            charge_dict = {
                "name": oeci_charge.name,
                "statute": oeci_charge.statute,
                "level": oeci_charge.level,
                "date": oeci_charge.date,
                "disposition": oeci_charge.disposition,
                "probation_revoked": oeci_charge.probation_revoked,
                "case_number": oeci_case.summary.case_number,
                "violation_type": oeci_case.summary.violation_type,
                "birth_year": oeci_case.summary.birth_year,
            }
            ambiguous_charge, question = ChargeCreator.create(ambiguous_charge_id, **charge_dict)
            ambiguous_charges.append(ambiguous_charge)
            if question:
                questions.append(question)
        ambiguous_charges += [[charge] for charge in new_charges]
        ambiguous_case: AmbiguousCase = []
        for charges in product(*ambiguous_charges):
            possible_case = Case(oeci_case.summary, charges=tuple(charges))
            ambiguous_case.append(possible_case)
        return ambiguous_case, questions

    @staticmethod
    def _find_unknown_dispositions(cases: List[OeciCase]) -> List[str]:
        unknown_dispositions = []
        for case in cases:
            for charge in case.charges:
                if charge.disposition.status in [DispositionStatus.UNRECOGNIZED, DispositionStatus.UNKNOWN]:
                    unknown_dispositions.append(charge.ambiguous_charge_id)
        return unknown_dispositions

    @staticmethod
    def _filter_for_blocking_charges(cases: Tuple[Case, ...], charge_ids: List[str]) -> List[str]:
        unknown_dispositions = []
        for case in cases:
            for charge in case.charges:
                if charge.ambiguous_charge_id in charge_ids and charge.charge_type.blocks_other_charges:
                    unknown_dispositions.append(charge.ambiguous_charge_id)
        return unknown_dispositions
