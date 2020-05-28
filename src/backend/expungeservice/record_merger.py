from dataclasses import replace
from expungeservice.util import DateWithFuture as date
from typing import List, Dict, Optional

from more_itertools import flatten, unique_everseen

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.models.case import Case
from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.sex_crimes import RomeoAndJulietNMASexCrime
from expungeservice.models.expungement_result import (
    TimeEligibility,
    ExpungementResult,
    TypeEligibility,
    EligibilityStatus,
    ChargeEligibility,
    ChargeEligibilityStatus,
)
from expungeservice.models.record import Record, Question
import collections


class RecordMerger:
    # We assume all records contain the same errors
    @staticmethod
    def merge(
        ambiguous_record: AmbiguousRecord,
        ambiguous_charge_id_to_time_eligibility_list: List[Dict[str, TimeEligibility]],
    ) -> Record:
        ambiguous_charge_id_to_time_eligibilities: Dict[str, List[TimeEligibility]] = collections.defaultdict(list)
        for charge_id_to_time_eligibility in ambiguous_charge_id_to_time_eligibility_list:
            for k, v in charge_id_to_time_eligibility.items():
                if v not in ambiguous_charge_id_to_time_eligibilities[k]:
                    ambiguous_charge_id_to_time_eligibilities[k].append(v)
        charges = list(flatten([record.charges for record in ambiguous_record]))
        record = ambiguous_record[0]
        new_case_list: List[Case] = []
        for case in record.cases:
            new_charges = []
            for charge in case.charges:
                time_eligibilities = ambiguous_charge_id_to_time_eligibilities.get(charge.ambiguous_charge_id)
                same_charges = list(filter(lambda c: c.ambiguous_charge_id == charge.ambiguous_charge_id, charges))
                romeo_and_juliet_exception = RecordMerger._is_romeo_and_juliet_exception(same_charges)
                merged_type_eligibility = RecordMerger.merge_type_eligibilities(same_charges)
                merged_time_eligibility = RecordMerger.merge_time_eligibilities(time_eligibilities)
                charge_eligibility = RecordMerger.compute_charge_eligibility(
                    merged_type_eligibility, time_eligibilities, romeo_and_juliet_exception
                )
                expungement_result = ExpungementResult(
                    type_eligibility=merged_type_eligibility,
                    time_eligibility=merged_time_eligibility,
                    charge_eligibility=charge_eligibility,
                )
                merged_type_name = " ⬥ ".join(
                    list(unique_everseen([charge.charge_type.type_name for charge in same_charges]))
                )
                merged_charge_type = replace(charge.charge_type, type_name=merged_type_name)
                new_charge: Charge = replace(
                    charge, charge_type=merged_charge_type, expungement_result=expungement_result
                )
                new_charges.append(new_charge)
            new_case = replace(case, charges=tuple(new_charges))
            new_case_list.append(new_case)
        return replace(record, cases=tuple(new_case_list))

    @staticmethod
    def filter_ambiguous_record(ambiguous_record: AmbiguousRecord, questions: List[Question]) -> AmbiguousRecord:
        records = []
        for record in ambiguous_record:
            if RecordMerger._is_possible_record(record, questions):
                records.append(record)
        return records

    @staticmethod
    def _is_possible_record(record: Record, questions: List[Question]):
        charges = record.charges
        charge_ids = list(map(lambda c: c.id, charges))
        for question in questions:
            if question.answer:
                not_answer_ids = [option_id for option_id in question.options.values() if option_id != question.answer]
                for not_answer_id in not_answer_ids:
                    if not_answer_id in charge_ids:
                        return False
        return True

    @staticmethod
    def merge_type_eligibilities(same_charges: List[Charge]) -> TypeEligibility:
        status = RecordMerger.compute_type_eligibility_status(same_charges)
        reasons = [charge.type_eligibility.reason for charge in same_charges]
        reason = " ⬥ ".join(list(unique_everseen(reasons)))
        return TypeEligibility(status=status, reason=reason)

    @staticmethod
    def compute_type_eligibility_status(charges: List[Charge]):
        if all([charge.type_eligibility.status == EligibilityStatus.ELIGIBLE for charge in charges]):
            return EligibilityStatus.ELIGIBLE
        elif all([charge.type_eligibility.status == EligibilityStatus.INELIGIBLE for charge in charges]):
            return EligibilityStatus.INELIGIBLE
        else:
            return EligibilityStatus.NEEDS_MORE_ANALYSIS

    @staticmethod
    def merge_time_eligibilities(time_eligibilities: Optional[List[TimeEligibility]]) -> Optional[TimeEligibility]:
        if time_eligibilities:
            status = RecordMerger.compute_time_eligibility_status(time_eligibilities)
            reasons = [time_eligibility.reason for time_eligibility in time_eligibilities]
            reason = " ⬥ ".join(list(unique_everseen(reasons)))
            date_will_be_eligible = time_eligibilities[0].date_will_be_eligible
            if len(set([time_eligibility.date_will_be_eligible for time_eligibility in time_eligibilities])) == 1:
                unique_date = True
            else:
                unique_date = False
            return TimeEligibility(
                status=status, reason=reason, date_will_be_eligible=date_will_be_eligible, unique_date=unique_date
            )
        else:
            return None

    @staticmethod
    def compute_time_eligibility_status(time_eligibilities: List[TimeEligibility]):
        if all([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]):
            return EligibilityStatus.ELIGIBLE
        else:
            return EligibilityStatus.INELIGIBLE

    # TODO: Think about if it is possible for a NEEDS_MORE_ANALYSIS type eligibility charge to have no disposition and handle.
    @staticmethod
    def compute_charge_eligibility(
        type_eligibility: TypeEligibility,
        time_eligibilities: Optional[List[TimeEligibility]],
        romeo_and_juliet_exception: bool = False,
    ) -> ChargeEligibility:
        if romeo_and_juliet_exception:
            return ChargeEligibility(ChargeEligibilityStatus.POSSIBLY_ELIGIBILE, "Possibly Eligible")
        elif type_eligibility.status == EligibilityStatus.INELIGIBLE:
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible")
        elif not time_eligibilities:
            return ChargeEligibility(ChargeEligibilityStatus.UNKNOWN, "Possibly eligible but time analysis is missing")
        elif all([time_eligibility.date_will_be_eligible == date.max() for time_eligibility in time_eligibilities]):
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible")
        elif any([time_eligibility.date_will_be_eligible == date.max() for time_eligibility in time_eligibilities]):
            at_least_will_be_eligibles = [
                time_eligibility
                for time_eligibility in time_eligibilities
                if time_eligibility.date_will_be_eligible != date.max()
            ]
            will_be_eligibles = [
                time_eligibility.date_will_be_eligible.strftime("%b %-d, %Y")
                for time_eligibility in at_least_will_be_eligibles
                if time_eligibility.status != EligibilityStatus.ELIGIBLE
            ]
            will_be_eligibles_string = " ⬥ ".join(will_be_eligibles)
            if all(
                [
                    time_eligibility.status == EligibilityStatus.ELIGIBLE
                    for time_eligibility in at_least_will_be_eligibles
                ]
            ):
                return ChargeEligibility(ChargeEligibilityStatus.POSSIBLY_ELIGIBILE, f"Possibly Eligible Now (review)")
            elif any(
                [
                    time_eligibility.status == EligibilityStatus.ELIGIBLE
                    for time_eligibility in at_least_will_be_eligibles
                ]
            ):
                return ChargeEligibility(
                    ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                    f"Possibly Eligible Now ⬥ {will_be_eligibles_string} (review)",
                )
            else:
                return ChargeEligibility(
                    ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                    f"Possibly Eligible {will_be_eligibles_string} (review)",
                )
        elif all([time_eligibility.date_will_be_eligible != date.max for time_eligibility in time_eligibilities]):
            if all([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]):
                return ChargeEligibility(ChargeEligibilityStatus.ELIGIBLE_NOW, "Eligible")
            else:
                will_be_eligibles = [
                    time_eligibility.date_will_be_eligible.strftime("%b %-d, %Y")
                    for time_eligibility in time_eligibilities
                    if time_eligibility.status != EligibilityStatus.ELIGIBLE
                ]
                eligible_date_string = " ⬥ ".join(will_be_eligibles)
                if any(
                    [time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]
                ):
                    return ChargeEligibility(
                        ChargeEligibilityStatus.WILL_BE_ELIGIBLE, f"Eligible Now ⬥ {eligible_date_string}"
                    )
                else:
                    return ChargeEligibility(
                        ChargeEligibilityStatus.WILL_BE_ELIGIBLE, f"Eligible {eligible_date_string}"
                    )
        else:
            raise ValueError("Either all, some, or no time eligibilities will have an eligibility date of date.max.")

    @staticmethod
    def _is_romeo_and_juliet_exception(same_charges: List[Charge]) -> bool:
        for charge in same_charges:
            if isinstance(charge.charge_type, RomeoAndJulietNMASexCrime):
                return True
        return False
