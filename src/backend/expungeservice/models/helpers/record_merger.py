from dataclasses import replace
from datetime import date
from typing import List, Dict, Set, Optional

from more_itertools import flatten, unique_everseen

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import (
    TimeEligibility,
    ExpungementResult,
    TypeEligibility,
    EligibilityStatus,
    ChargeEligibility,
    ChargeEligibilityStatus,
)
from expungeservice.models.record import Record
import collections


class RecordMerger:
    @staticmethod
    def merge(
        ambiguous_record: AmbiguousRecord, charge_id_to_time_eligibility_list: List[Dict[str, TimeEligibility]]
    ) -> Record:
        charge_id_to_time_eligibilities: Dict[str, Set[TimeEligibility]] = collections.defaultdict(set)
        for charge_id_to_time_eligibility in charge_id_to_time_eligibility_list:
            for k, v in charge_id_to_time_eligibility.items():
                charge_id_to_time_eligibilities[k].add(v)
        charges = list(flatten([record.charges for record in ambiguous_record]))
        record = ambiguous_record[0]
        new_case_list = []
        for case in record.cases:
            new_charges = []
            for charge in case.charges:
                time_eligibilities = charge_id_to_time_eligibilities.get(charge.id)
                same_charges = list(filter(lambda c: c.id == charge.id, charges))
                merged_type_eligibility = RecordMerger.merge_type_eligibilities(same_charges)
                merged_time_eligibility = RecordMerger.merge_time_eligibilities(time_eligibilities)
                charge_eligibility = RecordMerger.compute_charge_eligibility(
                    merged_type_eligibility, time_eligibilities
                )
                expungement_result = ExpungementResult(
                    type_eligibility=merged_type_eligibility,
                    time_eligibility=merged_time_eligibility,
                    charge_eligibility=charge_eligibility,
                )
                merged_type_name = " OR ".join(list(unique_everseen([charge.type_name for charge in same_charges])))
                new_charge: Charge = replace(charge, type_name=merged_type_name, expungement_result=expungement_result)
                new_charges.append(new_charge)
            new_case = replace(case, charges=new_charges)
            new_case_list.append(new_case)
        return replace(record, cases=new_case_list)

    @staticmethod
    def merge_type_eligibilities(same_charges: List[Charge]) -> TypeEligibility:
        status = RecordMerger.compute_type_eligibility_status(same_charges)
        reasons = [charge.type_eligibility.reason for charge in same_charges]
        reason = " OR ".join(list(unique_everseen(reasons)))
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
    def merge_time_eligibilities(time_eligibilities: Optional[Set[TimeEligibility]]) -> Optional[TimeEligibility]:
        if time_eligibilities:
            status = RecordMerger.compute_time_eligibility_status(time_eligibilities)
            reasons = [time_eligibility.reason for time_eligibility in time_eligibilities]
            reason = " OR ".join(list(unique_everseen(reasons)))
            date_will_be_eligible = date.max  # TODO: Fix
            return TimeEligibility(status=status, reason=reason, date_will_be_eligible=date_will_be_eligible)
        else:
            return None

    @staticmethod
    def compute_time_eligibility_status(time_eligibilities: Set[TimeEligibility]):
        if all([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]):
            return EligibilityStatus.ELIGIBLE
        else:
            return EligibilityStatus.INELIGIBLE

    # TODO: Think about if it is possible for a NEEDS_MORE_ANALYSIS type eligibility charge to have no disposition and handle.
    @staticmethod
    def compute_charge_eligibility(
        type_eligibility: TypeEligibility, time_eligibilities: Optional[Set[TimeEligibility]]
    ) -> ChargeEligibility:
        if type_eligibility.status == EligibilityStatus.INELIGIBLE:
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible")
        elif not time_eligibilities:
            return ChargeEligibility(ChargeEligibilityStatus.UNKNOWN, "Possibly eligible but time analysis is missing")
        elif all([time_eligibility.date_will_be_eligible == date.max for time_eligibility in time_eligibilities]):
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible")
        elif any([time_eligibility.date_will_be_eligible == date.max for time_eligibility in time_eligibilities]):
            at_least_will_be_eligibles = [
                time_eligibility
                for time_eligibility in time_eligibilities
                if time_eligibility.date_will_be_eligible != date.max
            ]
            will_be_eligibles = [
                time_eligibility.date_will_be_eligible.strftime("%b %-d, %Y")
                for time_eligibility in at_least_will_be_eligibles
                if time_eligibility.status != EligibilityStatus.ELIGIBLE
            ]
            will_be_eligibles_string = ", ".join(will_be_eligibles)
            if all(
                [
                    time_eligibility.status == EligibilityStatus.ELIGIBLE
                    for time_eligibility in at_least_will_be_eligibles
                ]
            ):
                return ChargeEligibility(ChargeEligibilityStatus.POSSIBLY_ELIGIBILE, f"Possibly Eligible (review)")
            elif any(
                [
                    time_eligibility.status == EligibilityStatus.ELIGIBLE
                    for time_eligibility in at_least_will_be_eligibles
                ]
            ):
                return ChargeEligibility(
                    ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                    f"Possibly Eligible Now, {will_be_eligibles_string} (review)",
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
                date_will_be_eligibles = [
                    time_eligibility.date_will_be_eligible.strftime("%b %-d, %Y")
                    for time_eligibility in time_eligibilities
                ]
                eligible_date_string = ", ".join(date_will_be_eligibles)
                return ChargeEligibility(ChargeEligibilityStatus.WILL_BE_ELIGIBLE, f"Eligible {eligible_date_string}")
        else:
            raise ValueError("Either all, some, or no time eligibilities will have an eligibility date of date.max.")
