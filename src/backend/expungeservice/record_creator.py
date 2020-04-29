from dataclasses import replace
from functools import lru_cache
from itertools import product, groupby
from typing import List, Dict, Tuple, Any, Callable
from datetime import datetime

import requests

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase, AmbiguousRecord
from expungeservice.models.case import Case, OeciCase, CaseCreator
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Question, Alias
from expungeservice.request import error
from expungeservice.models.disposition import DispositionCreator


class RecordCreator:
    @staticmethod
    def build_record(
        search: Callable,
        username: str,
        password: str,
        aliases: Tuple[Alias, ...],
        edits: Dict[str, Dict[str, Any]],
    ) -> Tuple[Record, AmbiguousRecord, Dict[str, Question]]:
        search_results, errors = search(username, password, aliases)
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
            user_edited_search_results = RecordCreator._edit_search_results(
                cases_with_unique_case_number, edits
            )
            ambiguous_record, questions = RecordCreator.build_ambiguous_record(user_edited_search_results)
            record = RecordCreator.analyze_ambiguous_record(ambiguous_record)
            questions_as_dict = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions)))
            return record, ambiguous_record, questions_as_dict

    # TODO: In the future we will add a cache here
    @staticmethod
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

    @staticmethod
    def _edit_search_results(search_result_cases: List[OeciCase], edits) -> List[OeciCase]:
        edited_cases: List[OeciCase] = []
        for case in search_result_cases:
            case_number = case.summary.case_number
            if case_number in edits.keys():
                if edits[case_number]["action"] == "edit":
                    edited_cases.append(RecordCreator._edit_case(case, edits[case_number]))
                # else: if the action name for this case_number isn't "edit", assume it is "delete" and skip it
            else:
                edited_cases.append(case)
        return edited_cases

    @staticmethod
    def _edit_case(case, edits):
        if "summary" in edits.keys():
            case_summary_edits: Dict[str, Any] = {}
            for key, value in edits["summary"].items():
                if key in ("date", "probation_revoked"):
                    case_summary_edits[key] = datetime.date(datetime.strptime(value, "%m/%d/%Y"))
                elif key == "balance_due":
                    case_summary_edits["balance_due_in_cents"] = CaseCreator.compute_balance_due_in_cents(value)
                elif key == "birth_year":
                    case_summary_edits["birth_year"] = int(value)
                else:
                    case_summary_edits[key] = value
            edited_summary = replace(case.summary, **case_summary_edits)
        else:
            edited_summary = case.summary
        if "charges" in edits.keys():
            edited_charges = RecordCreator._edit_charges(case.charges, edits["charges"])
        else:
            edited_charges = case.charges
        return OeciCase(edited_summary, edited_charges)

    @staticmethod
    def _edit_charges(charges, edits):
        edited_charges = []
        for charge in charges:
            # TODO: deleting charges not supported yet
            if charge.id in edits.keys():
                charge_edits: Dict[str, Any] = {}
                for key, value in edits[charge.id].items():
                    if key == "disposition":
                        charge_edits["disposition"] = DispositionCreator.create(
                            datetime.date(datetime.strptime(edits[charge.id]["disposition"]["date"], "%m/%d/%Y")),
                            edits[charge.id]["disposition"]["ruling"],
                        )
                    elif key == "date":
                        charge_edits["date"] = datetime.date(datetime.strptime(value, "%m/%d/%Y"))
                    else:
                        charge_edits[key] = value
                edited_charges.append(replace(charge, **charge_edits))
            else:
                edited_charges.append(charge)
        return edited_charges
