from dataclasses import replace

from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.util import DateWithFuture as date
from functools import lru_cache
from typing import Set, List, Tuple, Dict, Optional

from dateutil.relativedelta import relativedelta
from more_itertools import padnone, take

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaUnder21, MarijuanaViolation
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import EligibilityStatus, TimeEligibility
from expungeservice.models.record import Record


class Expunger:
    @staticmethod
    @lru_cache(maxsize=32)
    def run(record: Record, today: date = date.today()) -> Dict[str, TimeEligibility]:
        """
        Evaluates the expungement eligibility of a record.
        """
        analyzable_record = Expunger._without_skippable_charges(record)
        ambiguous_charge_id_to_time_eligibility = {}
        cases = analyzable_record.cases
        for charge in analyzable_record.charges:
            eligibility_dates: List[Tuple[date, str]] = []

            other_charges = [
                c for c in analyzable_record.charges if c.id != charge.id and c.edit_status != EditStatus.DELETE
            ]

            other_blocking_charges = [c for c in other_charges if c.charge_type.blocks_other_charges]

            convictions = [c for c in other_charges if c.convicted()]
            blocking_convictions = [c for c in other_blocking_charges if c.convicted()]

            most_recent_blocking_conviction = Expunger._most_recent_convictions(blocking_convictions)

            other_convictions_all_traffic = Expunger._is_other_convictions_all_traffic(convictions)

            if charge.convicted():
                if isinstance(charge.charge_type, MarijuanaUnder21) and other_convictions_all_traffic:
                    eligibility_dates.append(
                        (
                            charge.disposition.date + relativedelta(years=1),
                            "One year from date of conviction (137.226)",
                        )
                    )
                else:
                    eligibility_dates.append(
                        Expunger._single_conviction_years_by_level(charge.level, charge.disposition.date)
                    )
            elif charge.dismissed():
                eligibility_dates.append((charge.date, "Eligible immediately (137.225(1)(b))"))
            else:
                raise ValueError("Charge should always convicted or dismissed at this point.")

            if charge.type_eligibility.status == EligibilityStatus.INELIGIBLE:
                eligibility_dates.append((date.max(), "Never. Type ineligible charges are always time ineligible."))

            if charge.disposition.status == DispositionStatus.NO_COMPLAINT:
                eligibility_dates.append(
                    (
                        charge.disposition.date + relativedelta(days=60),
                        "Sixty days from date of no-complaint disposition (137.225(1)(c))",
                    )
                )

            if charge.convicted() and charge.probation_revoked:
                eligibility_dates.append(
                    (
                        charge.probation_revoked + relativedelta(years=10),
                        "Time-ineligible under 137.225(1)(c) (Probation Revoked). Inspect further if the case has multiple convictions on the case.",
                    )
                )

            if charge.convicted() and most_recent_blocking_conviction:
                relative_case_summary = most_recent_blocking_conviction.case(cases).summary
                blocking_convictions_time_eligibility = Expunger._other_blocking_conviction_years_by_level(charge.level, most_recent_blocking_conviction.disposition.date, relative_case_summary)
                eligibility_dates.append(blocking_convictions_time_eligibility)

            if isinstance(charge.charge_type, MarijuanaViolation):
                date_will_be_eligible = charge.disposition.date
                reason = "Eligible immediately (475B.401)"
            else:
                date_will_be_eligible, reason = max(eligibility_dates)

            if date_will_be_eligible and today >= date_will_be_eligible:
                time_eligibility = TimeEligibility(
                    status=EligibilityStatus.ELIGIBLE,
                    reason="Eligible now",
                    date_will_be_eligible=date_will_be_eligible,
                )
            else:
                time_eligibility = TimeEligibility(
                    status=EligibilityStatus.INELIGIBLE, reason=reason, date_will_be_eligible=date_will_be_eligible
                )
            ambiguous_charge_id_to_time_eligibility[charge.ambiguous_charge_id] = time_eligibility
        return ambiguous_charge_id_to_time_eligibility

    @staticmethod
    def _single_conviction_years_by_level(charge_level, charge_date):
        if "Felony Class A" in charge_level:
            return (
                date.max(),
                "Never. Type ineligible charges are always time ineligible."
            )
        elif "Felony Class B" in charge_level:
            return (
                charge_date + relativedelta(years=7),
                "Seven years from date of conviction (137.225(1)(a))",
            )
        elif "Felony Class C" in charge_level:
            return (
                charge_date + relativedelta(years=5),
                "Five years from date of conviction (137.225(1)(a))",
            )
        elif "Misdemeanor Class A" in charge_level:
            return (
                charge_date + relativedelta(years=3),
                "Three years from date of conviction (137.225(1)(a))",
            )
        elif any([level in charge_level for level in ["Misdemeanor Class B", "Misdemeanor Class C", "Violation"]]):
            return (
                charge_date + relativedelta(years=1),
                "One year from date of conviction (137.225(1)(a))",
            )
        elif "Misdemeanor" in charge_level: # TODO: Is an unspecified Misdemeanor always a Class A?
            return (
                charge_date + relativedelta(years=3),
                "Three years from date of conviction (137.225(1)(a))",
            )
        else:
            return (
                date.max(),
                f"Error: unrecognized severity level in \"{charge_level}\". Edit this charge to have a valid level."
            )

    @staticmethod
    def _other_blocking_conviction_years_by_level(target_charge_level, most_recent_blocking_conviction_date, relative_case_summary):
        potential = "potential " if not relative_case_summary.closed() else ""
        case_number = relative_case_summary.case_number
        # Skip Felony Class A because it's already covered by the self-blocking "never" rule.
        if "Felony Class B" in target_charge_level:
            return (
                most_recent_blocking_conviction_date + relativedelta(years=7),
                f"137.225(7)(b) – Seven years from most recent {potential}other conviction from case [{case_number}].",
            )
        elif "Felony Class C" in target_charge_level:
            return (
                most_recent_blocking_conviction_date + relativedelta(years=5),
                f"137.225(7)(b) – Five years from most recent {potential}other conviction from case [{case_number}].",
            )
        elif "Misdemeanor Class A" in target_charge_level:
            return (
                most_recent_blocking_conviction_date + relativedelta(years=3),
                f"137.225(7)(b) – Three years from most recent {potential}other conviction from case [{case_number}].",
            )
        elif any([level in target_charge_level for level in ["Misdemeanor Class B", "Misdemeanor Class C", "Violation"]]):
            return (
                most_recent_blocking_conviction_date + relativedelta(years=1),
                f"137.225(7)(b) – One year from most recent {potential}other conviction from case [{case_number}].",
            )
        elif "Misdemeanor" in target_charge_level: # TODO: Is an unspecified Misdemeanor always a Class A?
            return (
                most_recent_blocking_conviction_date + relativedelta(years=3),
                f"137.225(7)(b) – Three years from most recent {potential} other conviction from case [{case_number}].",
            )
        else:
            return (
                date.max(),
                f"Error: unrecognized severity level in \"{target_charge_level}\". Edit this charge to have a valid level."
            )
    @staticmethod
    def _most_recent_convictions(recent_convictions) -> Optional[Charge]:
        recent_convictions.sort(key=lambda charge: charge.disposition.date, reverse=True)
        newer, older = take(2, padnone(recent_convictions))
        if newer and "violation" in newer.level.lower():
            return older
        else:
            return newer

    @staticmethod
    def _is_other_convictions_all_traffic(convictions):
        for charge in convictions:
            if not isinstance(charge.charge_type, TrafficViolation):
                return False
        return True

    @staticmethod
    def _without_skippable_charges(record: Record) -> Record:
        updated_cases = []
        for case in record.cases:
            updated_charges = []
            for charge in case.charges:
                if (charge.convicted() or charge.dismissed()) and not isinstance(charge.charge_type, JuvenileCharge):
                    updated_charges.append(charge)
            updated_case = replace(case, charges=tuple(updated_charges))
            updated_cases.append(updated_case)
        return replace(record, cases=tuple(updated_cases))


class ErrorChecker:
    @staticmethod
    def check(record) -> List[str]:
        errors: List[str] = []
        open_cases = [case for case in record.cases if ErrorChecker.is_meaningfully_open_case(case)]
        if len(open_cases) > 0:
            case_numbers = ", ".join([f"[{case.summary.case_number}]" for case in open_cases])
            errors += [
                f"All charges are ineligible because there is one or more open case: {case_numbers}. Open cases containing charges with valid dispositions are still included in time analysis. Otherwise they are ignored, so time analysis may be inaccurate for other charges."
            ]
        errors += ErrorChecker._build_disposition_errors(record.charges, record.cases)
        errors += ErrorChecker._build_unclassified_charge_errors(record.charges)
        return errors

    @staticmethod
    def is_meaningfully_open_case(case: Case) -> bool:
        closed = case.summary.closed()
        if closed:
            return False
        else:
            return any(ErrorChecker.is_meaningfully_open_charge(charge) for charge in case.charges)

    @staticmethod
    def is_meaningfully_open_charge(charge: Charge) -> bool:
        is_not_violation = not isinstance(charge.charge_type, Violation)
        charge_with_invalid_disposition = charge.disposition.status in [
            DispositionStatus.UNKNOWN,
            DispositionStatus.UNRECOGNIZED,
        ]
        return charge.charge_type.blocks_other_charges and is_not_violation and charge_with_invalid_disposition

    @staticmethod
    def _build_disposition_errors(charges: List[Charge], cases: List[Case]):
        record_errors = []
        cases_with_missing_disposition, cases_with_unrecognized_disposition = ErrorChecker._filter_cases_with_errors(
            charges, cases
        )
        if cases_with_missing_disposition:
            record_errors.append(ErrorChecker._build_missing_disposition_error_message(cases_with_missing_disposition))
        if cases_with_unrecognized_disposition:
            record_errors.append(
                ErrorChecker._build_unrecognized_disposition_error_message(cases_with_unrecognized_disposition)
            )
        return record_errors

    @staticmethod
    def _filter_cases_with_errors(charges: List[Charge], cases: List[Case]):
        cases_with_missing_disposition: Set[str] = set()
        cases_with_unrecognized_disposition: Set[Tuple[str, str]] = set()
        for charge in charges:
            if charge.charge_type.blocks_other_charges:
                case_number = f"[{charge.case(cases).summary.case_number}]"
                if charge.disposition.status == DispositionStatus.UNKNOWN and charge.case(cases).summary.closed():
                    cases_with_missing_disposition.add(case_number)
                elif charge.disposition.status == DispositionStatus.UNRECOGNIZED:
                    cases_with_unrecognized_disposition.add((case_number, charge.disposition.ruling))
        return cases_with_missing_disposition, cases_with_unrecognized_disposition

    @staticmethod
    def _build_missing_disposition_error_message(error_cases: Set[str]):
        if len(error_cases) == 1:
            error_message = f"""Case {error_cases.pop()} has a charge with a missing disposition.
This might be an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges."""
        else:
            cases_list_string = ", ".join(error_cases)
            error_message = f"""The following cases have charges with a missing disposition.
This might be an error in the OECI database. Time analysis is ignoring these charges and may be inaccurate for other charges.
Case numbers: {cases_list_string}"""
        return error_message

    @staticmethod
    def _build_unrecognized_disposition_error_message(error_cases_with_rulings: Set[Tuple[str, str]]):
        if len(error_cases_with_rulings) == 1:
            error_message = f"""Case {next(iter(error_cases_with_rulings))[0]} has a charge with an unrecognized disposition ({next(iter(error_cases_with_rulings))[1]}).
This might be an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges."""
        else:
            cases_list_string = ", ".join([pair[0] + " (" + pair[1] + ")" for pair in error_cases_with_rulings])
            error_message = f"""The following cases have charges with an unrecognized disposition.
This might be an error in the OECI database. Time analysis is ignoring these charges and may be inaccurate for other charges.
Case numbers: {cases_list_string}"""
        return error_message

    @staticmethod
    def _build_unclassified_charge_errors(charges: List[Charge]) -> List[str]:
        record_errors = []
        for charge in charges:
            if isinstance(charge.charge_type, UnclassifiedCharge):
                message = f"Case [{charge.case_number}] has a charge that RecordSponge could not classify. Please enable editing to choose a charge type. Also please report this issue to help@recordsponge.com."
                record_errors.append(message)
        return record_errors
