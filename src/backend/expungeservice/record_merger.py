from dataclasses import replace
from expungeservice.util import DateWithFuture as date
from typing import List, Dict, Optional

from more_itertools import flatten, unique_everseen

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.models.case import Case
from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.sex_crimes import RomeoAndJulietNMASexCrime
from expungeservice.models.disposition import Disposition, DispositionCreator
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
    # We assume all records contain the same errors
    @staticmethod
    def merge(
        ambiguous_record: AmbiguousRecord,
        ambiguous_charge_id_to_time_eligibility_list: List[Dict[str, TimeEligibility]],
        charge_ids_with_question: List[str],
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
                sorted_time_eligibility = (
                    sorted(time_eligibilities, key=lambda e: e.date_will_be_eligible) if time_eligibilities else None
                )
                same_charges = list(filter(lambda c: c.ambiguous_charge_id == charge.ambiguous_charge_id, charges))
                romeo_and_juliet_exception = RecordMerger._is_romeo_and_juliet_exception(same_charges)
                merged_type_eligibility = RecordMerger.merge_type_eligibilities(same_charges)
                merged_time_eligibility = RecordMerger.merge_time_eligibilities(sorted_time_eligibility)
                if charge.ambiguous_charge_id in charge_ids_with_question:
                    charge_eligibility = ChargeEligibility(
                        ChargeEligibilityStatus.NEEDS_MORE_ANALYSIS, "Needs More Analysis"
                    )
                else:
                    charge_eligibility = RecordMerger.compute_charge_eligibility(
                        merged_type_eligibility, sorted_time_eligibility, romeo_and_juliet_exception
                    )
                    if "open" in charge_eligibility.label.lower():
                        charge_eligibility = replace(
                            charge_eligibility,
                            label=f"Eligibility date dependent on open charge: {charge_eligibility.label}",
                        )
                if case.summary.restitution and charge_eligibility.status != ChargeEligibilityStatus.INELIGIBLE :
                    charge_eligibility = ChargeEligibility(
                        ChargeEligibilityStatus.INELIGIBLE_IF_RESTITUTION_OWED, "Ineligible If Restitution Owed"
                    )
                expungement_result = ExpungementResult(
                    type_eligibility=merged_type_eligibility,
                    time_eligibility=merged_time_eligibility,
                    charge_eligibility=charge_eligibility,
                )
                merged_type_name = " OR ".join(
                    list(unique_everseen([charge.charge_type.type_name for charge in same_charges]))
                )
                merged_charge_type = replace(charge.charge_type, type_name=merged_type_name)
                merged_disposition = RecordMerger.merge_dispositions(same_charges)
                new_charge: Charge = replace(
                    charge,
                    charge_type=merged_charge_type,
                    expungement_result=expungement_result,
                    disposition=merged_disposition,
                )
                new_charges.append(new_charge)
            new_case = replace(case, charges=tuple(new_charges))
            new_case_list.append(new_case)
        return replace(record, cases=tuple(new_case_list))

    @staticmethod
    def merge_type_eligibilities(same_charges: List[Charge]) -> TypeEligibility:
        status = RecordMerger.compute_type_eligibility_status(same_charges)
        reasons = [
            c.charge_type.type_name + " – " + c.type_eligibility.reason
            for c in list(unique_everseen(same_charges, lambda c: c.charge_type.type_name))
        ]
        reason = " OR ".join(reasons)
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
            reason = " OR ".join(list(unique_everseen(reasons)))
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

    # TODO: Sort labels
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
            # For example, JuvenileCharge
            return ChargeEligibility(ChargeEligibilityStatus.UNKNOWN, "Possibly Eligible")
        elif all([time_eligibility.date_will_be_eligible == date.max() for time_eligibility in time_eligibilities]):
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible")
        elif any([time_eligibility.date_will_be_eligible == date.max() for time_eligibility in time_eligibilities]):
            non_ineligibles = [
                time_eligibility
                for time_eligibility in time_eligibilities
                if time_eligibility.date_will_be_eligible != date.max()
            ]
            future_eligibles = [
                time_eligibility.date_will_be_eligible
                for time_eligibility in non_ineligibles
                if time_eligibility.status != EligibilityStatus.ELIGIBLE
            ]
            future_eligibles_strings = [d.strftime("%b %-d, %Y") for d in future_eligibles]
            future_eligibles_string = " or ".join(future_eligibles_strings)
            if all([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in non_ineligibles]):
                return ChargeEligibility(ChargeEligibilityStatus.POSSIBLY_ELIGIBILE, f"Possibly Eligible Now")
            elif any([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in non_ineligibles]):
                return ChargeEligibility(
                    ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                    f"Possibly Eligible Now or {future_eligibles_string}",
                    future_eligibles[0],
                )
            else:
                return ChargeEligibility(
                    ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                    f"Possibly Eligible {future_eligibles_string}",
                    future_eligibles[0],
                )
        elif all([time_eligibility.date_will_be_eligible != date.max for time_eligibility in time_eligibilities]):
            if all([time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]):
                return ChargeEligibility(ChargeEligibilityStatus.ELIGIBLE_NOW, "Eligible Now")
            else:
                future_eligibles = [
                    time_eligibility.date_will_be_eligible
                    for time_eligibility in time_eligibilities
                    if time_eligibility.status != EligibilityStatus.ELIGIBLE
                ]
                future_eligibles_strings = [d.strftime("%b %-d, %Y") for d in future_eligibles]
                eligible_date_string = " or ".join(future_eligibles_strings)
                if any(
                    [time_eligibility.status == EligibilityStatus.ELIGIBLE for time_eligibility in time_eligibilities]
                ):
                    return ChargeEligibility(
                        ChargeEligibilityStatus.WILL_BE_ELIGIBLE,
                        f"Eligible Now or {eligible_date_string}",
                        future_eligibles[0],
                    )
                else:
                    return ChargeEligibility(
                        ChargeEligibilityStatus.WILL_BE_ELIGIBLE,
                        f"Eligible {eligible_date_string}",
                        future_eligibles[0],
                    )
        else:
            raise ValueError("Either all, some, or no time eligibilities will have an eligibility date of date.max.")

    @staticmethod
    def _is_romeo_and_juliet_exception(same_charges: List[Charge]) -> bool:
        for charge in same_charges:
            if isinstance(charge.charge_type, RomeoAndJulietNMASexCrime):
                return True
        return False

    @staticmethod
    def merge_dispositions(same_charges: List[Charge]) -> Disposition:
        if len(list(unique_everseen([charge.disposition for charge in same_charges]))) == 2:
            return DispositionCreator.empty()
        else:
            return same_charges[0].disposition
