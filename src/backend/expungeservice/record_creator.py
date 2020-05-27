from dataclasses import replace, asdict
from functools import lru_cache
from itertools import product, groupby
from typing import List, Dict, Tuple, Any, Callable, Type
from datetime import datetime
from expungeservice.util import DateWithFuture as date_class

import requests
from dacite import from_dict

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.generator import get_charge_classes
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase, AmbiguousRecord
from expungeservice.models.case import Case, OeciCase, CaseCreator
from expungeservice.models.charge import OeciCharge, Charge
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Question, Alias
from expungeservice.request import error
from expungeservice.models.disposition import DispositionCreator, DispositionStatus


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
            user_edited_search_results, new_charges = RecordCreator._edit_search_results(
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
    def _edit_search_results(search_result_cases: List[OeciCase], edits) -> Tuple[List[OeciCase], List[Charge]]:
        edited_cases: List[OeciCase] = []
        new_charges_acc: List[Charge] = []
        for case in search_result_cases:
            case_number = case.summary.case_number
            if case_number in edits.keys():
                if edits[case_number]["action"] == "edit":
                    edited_case, new_charges = RecordCreator._edit_case(case, edits[case_number])
                    edited_cases.append(edited_case)
                    new_charges_acc += new_charges
                # else: if the action name for this case_number isn't "edit", assume it is "delete" and skip it
            else:
                edited_cases.append(case)
        return edited_cases, new_charges_acc

    @staticmethod
    def _edit_case(case: OeciCase, case_edits) -> Tuple[OeciCase, List[Charge]]:
        if "summary" in case_edits.keys():
            case_summary_edits: Dict[str, Any] = {}
            for key, value in case_edits["summary"].items():
                if key == "date":
                    case_summary_edits["date"] = date_class.fromdatetime(datetime.strptime(value, "%m/%d/%Y"))
                elif key == "balance_due":
                    case_summary_edits["balance_due_in_cents"] = CaseCreator.compute_balance_due_in_cents(value)
                elif key == "birth_year":
                    case_summary_edits["birth_year"] = int(value)
                else:
                    case_summary_edits[key] = value
            edited_summary = replace(case.summary, **case_summary_edits)
        else:
            edited_summary = case.summary
        new_charges: List[Charge] = []
        if "charges" in case_edits.keys():
            edited_charges, new_charges = RecordCreator._edit_charges(
                case.summary.case_number, case.charges, case_edits["charges"]
            )
        else:
            edited_charges = case.charges
        return OeciCase(edited_summary, edited_charges), new_charges

    @staticmethod
    def _edit_charges(
        case_number: str, charges: Tuple[OeciCharge, ...], charges_edits
    ) -> Tuple[Tuple[OeciCharge, ...], List[Charge]]:
        edited_charges, new_charges = [], []
        for charge in charges:
            # TODO: deleting charges not supported yet
            if charge.ambiguous_charge_id in charges_edits.keys():
                charge_edits = charges_edits[charge.ambiguous_charge_id]
                charge_dict = RecordCreator._parse_charge_edits(charge_edits)
                charge_type_string = charge_dict.pop("charge_type", None)
                edited_oeci_charge = replace(charge, **charge_dict)
                if charge_type_string:
                    charge_type = RecordCreator._get_charge_type(charge_type_string)
                    charge_type_data = {
                        "id": f"{charge.ambiguous_charge_id}-0",
                        "case_number": case_number,
                        **asdict(edited_oeci_charge),
                    }
                    new_charge = from_dict(data_class=charge_type, data=charge_type_data)
                    new_charges.append(new_charge)
                else:
                    edited_charges.append(edited_oeci_charge)
            else:
                edited_charges.append(charge)
        for ambiguous_charge_id, charge_edits in charges_edits.items():
            charge_ids = [charge.ambiguous_charge_id for charge in charges]
            if ambiguous_charge_id not in charge_ids:
                charge_dict = RecordCreator._parse_charge_edits(charge_edits)
                charge_type_string = charge_dict.pop("charge_type", None)
                charge_type = RecordCreator._get_charge_type(charge_type_string)
                charge_edits_with_defaults = {
                    **charge_dict,
                    "ambiguous_charge_id": ambiguous_charge_id,
                    "case_number": case_number,
                    "id": f"{ambiguous_charge_id}-0",
                    "name": "N/A",
                    "statute": "N/A",
                    "level": "N/A",
                    "type_name": "N/A",
                }
                new_charge = from_dict(data_class=charge_type, data=charge_edits_with_defaults)
                new_charges.append(new_charge)
        return tuple(edited_charges), new_charges

    @staticmethod
    def _get_charge_type(charge_type: str) -> Type[Charge]:
        charge_types = get_charge_classes()
        charge_types_dict = {charge_type.__name__: charge_type for charge_type in charge_types}
        return charge_types_dict.get(charge_type, UnclassifiedCharge)

    @staticmethod
    def _parse_charge_edits(charge_edits):
        charge_dict: Dict[str, Any] = {}
        for key, value in charge_edits.items():
            if key == "disposition":
                if value:
                    charge_dict["disposition"] = DispositionCreator.create(
                        date_class.fromdatetime(datetime.strptime(charge_edits["disposition"]["date"], "%m/%d/%Y")),
                        charge_edits["disposition"]["ruling"],
                    )
                else:
                    charge_dict["disposition"] = None
            elif key in ("date", "probation_revoked"):
                if value:
                    charge_dict[key] = date_class.fromdatetime(datetime.strptime(value, "%m/%d/%Y"))
            else:
                charge_dict[key] = value
        return charge_dict

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
                if charge.ambiguous_charge_id in charge_ids and charge.blocks_other_charges:
                    unknown_dispositions.append(charge.ambiguous_charge_id)
        return unknown_dispositions
