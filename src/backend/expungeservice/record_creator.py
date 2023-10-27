import operator
from dataclasses import replace
from functools import reduce
from itertools import product, groupby
from typing import List, Dict, Tuple, Any, Callable

import requests

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.expunger import ErrorChecker, Expunger
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase, AmbiguousRecord
from expungeservice.models.case import Case, OeciCase
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.record_editor import RecordEditor
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record, Alias, QuestionSummary, Question, Answer
from expungeservice.request import error
from expungeservice.models.disposition import DispositionStatus, DispositionCreator
from expungeservice.util import DateWithFuture as date_class, LRUCache


class RecordCreator:
    @staticmethod
    def build_record(
        search: Callable,
        username: str,
        password: str,
        aliases: Tuple[Alias, ...],
        edits: Dict[str, Dict[str, Any]],
        today: date_class,
        search_cache: LRUCache,
    ) -> Tuple[Record, Dict[str, QuestionSummary]]:
        search_results, errors = search(username, password, aliases, search_cache)
        if errors:
            record = Record((), tuple(errors))
            return record, {}
        else:
            cases_with_unique_case_number: List[OeciCase] = [
                list(group)[0]
                for key, group in groupby(
                    sorted(search_results, key=lambda case: case.summary.case_number),
                    lambda case: case.summary.case_number,
                )
            ]
            user_edited_search_results, new_charges = RecordEditor.edit_search_results(
                cases_with_unique_case_number, edits
            )

            ambiguous_cases, questions = RecordCreator._build_ambiguous_cases(user_edited_search_results, new_charges)

            ambiguous_record, overflow_error = RecordCreator._build_ambiguous_record(ambiguous_cases)
            if overflow_error:
                return Record((), tuple(overflow_error)), {}
            else:
                charge_ids_with_question = [question.ambiguous_charge_id for question in questions]
                record = RecordCreator._analyze_ambiguous_record(ambiguous_record, charge_ids_with_question, today)
                questions_as_dict = dict(list(map(lambda q: (q.ambiguous_charge_id, q), questions)))
                return record, questions_as_dict

    @staticmethod
    def build_search_results(
        username: str, password: str, aliases: Tuple[Alias, ...], search_cache: LRUCache
    ) -> Tuple[List[OeciCase], List[str]]:
        errors = []
        search_results: List[OeciCase] = []
        alias_match = search_cache[aliases]
        if alias_match:
            return alias_match
        else:
            for alias in aliases:
                session = requests.Session()
                try:
                    login_response = Crawler.attempt_login(session, username, password)
                    alias_search_result = Crawler.search(
                        session,
                        login_response,
                        alias.first_name,
                        alias.last_name,
                        alias.middle_name,
                        alias.birth_date,
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
            if not errors:
                search_cache[aliases] = search_results, errors
            return search_results, errors

    @staticmethod
    def _build_ambiguous_cases(
        search_result: List[OeciCase], new_charges: List[Charge]
    ) -> Tuple[List[AmbiguousCase], List[QuestionSummary]]:
        questions_accumulator: List[QuestionSummary] = []
        ambiguous_cases: List[AmbiguousCase] = []
        for oeci_case in search_result:
            new_charges_in_case = list(
                filter(lambda charge: charge.case_number == oeci_case.summary.case_number, new_charges)
            )
            ambiguous_case, questions = RecordCreator._build_case(oeci_case, new_charges_in_case)
            questions_accumulator += questions
            ambiguous_cases.append(ambiguous_case)
        return ambiguous_cases, questions_accumulator

    @staticmethod
    def _build_ambiguous_record(ambiguous_cases: List[AmbiguousCase]) -> Tuple[AmbiguousRecord, List[str]]:
        ambiguous_record_length = reduce(
            operator.mul, [len(ambiguous_case) for ambiguous_case in ambiguous_cases], 1
        )  # TODO: Replace with math.prod([len(ambiguous_case) for ambiguous_case in ambiguous_cases]) in Python 3.8
        MAX_EXPUNGER_RUNS = 128
        if ambiguous_record_length > MAX_EXPUNGER_RUNS:
            error_message = f"The resulting record found was too large to analyze (record with {ambiguous_record_length} combinations of ambiguities exceeds the processable {MAX_EXPUNGER_RUNS} combination of ambiguities). The record most likely has open cases, and thus does not have any charges eligible to be expunged."
            return [], [error_message]
        else:
            ambiguous_record: AmbiguousRecord = []
            for cases in product(*ambiguous_cases):
                ambiguous_record.append(Record(tuple(cases)))
            return ambiguous_record, []

    @staticmethod
    def _analyze_ambiguous_record(
        ambiguous_record: AmbiguousRecord, charge_ids_with_question: List[str], today: date_class
    ):
        charge_id_to_time_eligibilities = []
        ambiguous_record_with_errors = []
        for record in ambiguous_record:
            charge_id_to_time_eligibility = Expunger.run(record, today)
            charge_id_to_time_eligibilities.append(charge_id_to_time_eligibility)
            ambiguous_record_with_errors.append(record)
        record = RecordMerger.merge(
            ambiguous_record_with_errors, charge_id_to_time_eligibilities, charge_ids_with_question
        )
        sorted_record = RecordCreator.sort_record(record)
        return replace(sorted_record, errors=tuple(ErrorChecker.check(sorted_record)))

    @staticmethod
    def sort_record(record):
        updated_cases = []
        for case in record.cases:
            sorted_charges = sorted(case.charges, key=lambda charge: charge.ambiguous_charge_id)
            updated_case = replace(case, charges=tuple(sorted_charges))
            updated_cases.append(updated_case)
        record_with_sorted_charges = replace(record, cases=tuple(updated_cases))
        return RecordCreator.sort_record_by_case_date(record_with_sorted_charges)

    @staticmethod
    def sort_record_by_case_date(record):
        sorted_cases = sorted(record.cases, key=lambda case: case.summary.date, reverse=True)
        return replace(record, cases=tuple(sorted_cases))

    @staticmethod
    def _build_case(oeci_case: OeciCase, new_charges: List[Charge]) -> Tuple[AmbiguousCase, List[QuestionSummary]]:
        ambiguous_charges: List[AmbiguousCharge] = []
        questions: List[QuestionSummary] = []
        for oeci_charge in oeci_case.charges:
            ambiguous_charge_id = oeci_charge.ambiguous_charge_id
            charge_dict = {
                "name": oeci_charge.name,
                "statute": oeci_charge.statute,
                "level": oeci_charge.level,
                "date": oeci_charge.date,
                "disposition": oeci_charge.disposition,
                "probation_revoked": oeci_charge.probation_revoked,
                "balance_due_in_cents": oeci_charge.balance_due_in_cents,
                "case_number": oeci_case.summary.case_number,
                "violation_type": oeci_case.summary.violation_type,
                "location": oeci_case.summary.location,
                "birth_year": oeci_case.summary.birth_year,
                "edit_status": EditStatus(oeci_charge.edit_status),
            }
            if oeci_charge.disposition.status == DispositionStatus.UNKNOWN:
                charge_dict.pop("disposition")
                ambiguous_charge_dismissed, question_dismissed = ChargeCreator.create(
                    ambiguous_charge_id,
                    **charge_dict,
                    disposition=DispositionCreator.create(date_class.today(), "dismissed"),
                )
                ambiguous_charge_convicted, question_convicted = ChargeCreator.create(
                    ambiguous_charge_id,
                    **charge_dict,
                    disposition=DispositionCreator.create(date_class.future(), "convicted"),
                )
                if RecordCreator._disposition_question_is_irrelevant(
                    ambiguous_charge_convicted, ambiguous_charge_dismissed
                ):
                    ambiguous_charges.append(ambiguous_charge_dismissed)
                    question = RecordCreator._append_ambiguous_charge_id_to_question_id(question_dismissed, ambiguous_charge_id) if question_dismissed else None  # type: ignore # TODO: Fix type
                else:
                    ambiguous_charges.append(ambiguous_charge_dismissed + ambiguous_charge_convicted)
                    disposition_question_text = "Choose the disposition"
                    question_id_prefix = ambiguous_charge_id + disposition_question_text
                    dismissed_option = RecordCreator._build_option(
                        question_dismissed, "Dismissed", f"{question_id_prefix}-dismissed"
                    )
                    convicted_option = RecordCreator._build_option(
                        question_convicted, "Convicted", f"{question_id_prefix}-convicted"
                    )
                    probation_revoked_option = RecordCreator._build_probation_revoked_option(
                        question_convicted, f"{question_id_prefix}-revoked"
                    )
                    unknown_option = {"Unknown": Answer()}
                    question = Question(
                        question_id_prefix,
                        disposition_question_text,
                        {**dismissed_option, **convicted_option, **probation_revoked_option, **unknown_option},
                    )
            else:
                ambiguous_charge, maybe_question = ChargeCreator.create(ambiguous_charge_id, **charge_dict)
                ambiguous_charges.append(ambiguous_charge)
                question = RecordCreator._append_ambiguous_charge_id_to_question_id(maybe_question, ambiguous_charge_id) if maybe_question else None  # type: ignore # TODO: Fix type
            if question:
                question_summary = QuestionSummary(ambiguous_charge_id, oeci_case.summary.case_number, question)
                questions.append(question_summary)
        ambiguous_charges += [[charge] for charge in new_charges]
        ambiguous_case: AmbiguousCase = []
        for charges in product(*ambiguous_charges):
            possible_case = Case(oeci_case.summary, charges=tuple(charges))
            ambiguous_case.append(possible_case)
        return ambiguous_case, questions

    @staticmethod
    def _append_ambiguous_charge_id_to_question_id(question: Question, ambiguous_charge_id: str) -> Question:
        updated_options = {}
        for answer_string, answer in question.options.items():
            answer_question = (
                RecordCreator._append_ambiguous_charge_id_to_question_id(answer.question, ambiguous_charge_id)
                if answer.question
                else None
            )
            updated_answer = replace(answer, question=answer_question)
            updated_options[answer_string] = updated_answer
        return replace(question, question_id=f"{ambiguous_charge_id}-{question.question_id}", options=updated_options)

    @staticmethod
    def _build_option(question, ruling, question_id_prefix):
        disposition = {"disposition": {"date": "__DATE__", "ruling": ruling.lower()}}
        if question:
            updated_question = RecordCreator._append_edits_to_question(question, disposition, question_id_prefix)
            option = {ruling: Answer(question=updated_question)}
        else:
            option = {ruling: Answer(edit=disposition)}
        return option

    @staticmethod
    def _build_probation_revoked_option(question, question_id_prefix):
        edits = {
            "disposition": {"date": "__DATE__", "ruling": "convicted"},
            "probation_revoked": "__PROBATION_REVOKED_DATE__",
        }
        if question:
            updated_question = RecordCreator._append_edits_to_question(question, edits, question_id_prefix)
            option = {"Probation Revoked": Answer(question=updated_question)}
        else:
            option = {"Probation Revoked": Answer(edit=edits)}
        return option

    @staticmethod
    def _append_edits_to_question(question: Question, edits: Dict[str, Any], question_id_prefix: str) -> Question:
        updated_options = {}
        for answer_string, answer in question.options.items():
            updated_question = (
                RecordCreator._append_edits_to_question(answer.question, edits, question_id_prefix)
                if answer.question
                else None
            )
            updated_answer = replace(answer, question=updated_question, edit={**answer.edit, **edits})
            updated_options[answer_string] = updated_answer
        return replace(question, question_id=f"{question_id_prefix}-{question.question_id}", options=updated_options)

    @staticmethod
    def _disposition_question_is_irrelevant(ambiguous_charge_convicted, ambiguous_charge_dismissed):
        return (
            len(ambiguous_charge_convicted) == 1
            and len(ambiguous_charge_dismissed) == 1
            and ambiguous_charge_convicted[0].charge_type == ambiguous_charge_dismissed[0].charge_type
            and not ambiguous_charge_dismissed[0].charge_type.blocks_other_charges
        )  # TODO: Make assumption more explicit
