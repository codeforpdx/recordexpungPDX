from datetime import date
from typing import Set, List, Iterator, Tuple, Dict

from dateutil.relativedelta import relativedelta
from more_itertools import flatten, padnone, take

from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import EligibilityStatus, TimeEligibility
from expungeservice.models.record import Record


class Expunger:
    def __init__(self, record: Record):
        self.record = record
        self.analyzable_charges = Expunger._without_skippable_charges(self.record.charges)

    def run(self) -> Dict[str, TimeEligibility]:
        """
        Evaluates the expungement eligibility of a record.
        """
        charge_id_to_time_eligibility = {}
        for charge in self.analyzable_charges:
            eligibility_dates: List[Tuple[date, str]] = []
            other_charges = [c for c in self.analyzable_charges if c != charge and c.blocks_other_charges()]
            dismissals, convictions = Expunger._categorize_charges(other_charges)
            most_recent_blocking_dismissal = Expunger._most_recent_different_case_dismissal(charge, dismissals)
            most_recent_blocking_conviction = Expunger._most_recent_convictions(convictions)

            if charge.convicted():
                eligibility_dates.append(
                    (
                        charge.disposition.date + relativedelta(years=3),
                        "Three years from date of conviction (137.225(1)(a))",
                    )
                )

            elif charge.dismissed():
                eligibility_dates.append((charge.date, "Eligible immediately (137.225(1)(b))"))
            else:
                raise ValueError("Charge should always convicted or dismissed at this point.")

            if charge.type_eligibility.status == EligibilityStatus.INELIGIBLE:
                eligibility_dates.append((date.max, "Never. Type ineligible charges are always time ineligible."))

            if charge.disposition.status == DispositionStatus.NO_COMPLAINT:
                eligibility_dates.append(
                    (
                        charge.disposition.date + relativedelta(years=1),
                        "One year from date of no-complaint arrest (137.225(1)(b))",
                    )
                )

            if charge.convicted():
                probation_revoked_date = charge.case()().get_probation_revoked()
                if probation_revoked_date:
                    eligibility_dates.append(
                        (
                            probation_revoked_date + relativedelta(years=10),
                            "Time-ineligible under 137.225(1)(c). Inspect further if the case has multiple convictions on the case.",
                        )
                    )

            if most_recent_blocking_conviction:
                conviction_string = "other conviction" if charge.convicted() else "conviction"
                eligibility_dates.append(
                    (
                        most_recent_blocking_conviction.disposition.date + relativedelta(years=10),
                        f"Ten years from most recent {conviction_string} (137.225(7)(b))",
                    )
                )

            if charge.dismissed() and most_recent_blocking_dismissal:
                eligibility_dates.append(
                    (
                        most_recent_blocking_dismissal.date + relativedelta(years=3),
                        "Three years from most recent other arrest (137.225(8)(a))",
                    )
                )

            if charge.convicted() and isinstance(charge, FelonyClassB):
                if Expunger._calculate_has_subsequent_charge(charge, other_charges):
                    eligibility_dates.append(
                        (
                            date.max,
                            "Never. Class B felony can have no subsequent arrests or convictions (137.225(5)(a)(A)(ii))",
                        )
                    )
                else:
                    eligibility_dates.append((charge.disposition.date + relativedelta(years=20), "Twenty years from date of class B felony conviction (137.225(5)(a)(A)(i))"))  # type: ignore

            date_will_be_eligible, reason = max(eligibility_dates)
            if date_will_be_eligible and date.today() >= date_will_be_eligible:
                time_eligibility = TimeEligibility(
                    status=EligibilityStatus.ELIGIBLE,
                    reason="Eligible now",
                    date_will_be_eligible=date_will_be_eligible,
                )
            else:
                time_eligibility = TimeEligibility(
                    status=EligibilityStatus.INELIGIBLE, reason=reason, date_will_be_eligible=date_will_be_eligible
                )
            charge_id_to_time_eligibility[charge.id] = time_eligibility
        for case in self.record.cases:
            non_violation_convictions_in_case = []
            violations_in_case = []
            for charge in case.charges:
                if charge.convicted():
                    if "violation" in charge.level.lower():
                        violations_in_case.append(charge)
                    else:
                        non_violation_convictions_in_case.append(charge)
            violations_in_case.sort(key=lambda charge: charge.disposition.date, reverse=True)
            if len(non_violation_convictions_in_case) == 1 and len(violations_in_case) <= 1:
                attractor = non_violation_convictions_in_case[0]
            elif len(violations_in_case) == 1:
                attractor = violations_in_case[0]
            elif len(violations_in_case) in [2, 3]:
                attractor = violations_in_case[1]
            else:
                attractor = None

            if attractor:
                for charge in case.charges:
                    if (
                        charge.type_eligibility.status != EligibilityStatus.INELIGIBLE
                        and charge.dismissed()
                        and charge_id_to_time_eligibility[charge.id].date_will_be_eligible
                        > charge_id_to_time_eligibility[attractor.id].date_will_be_eligible
                    ):
                        time_eligibility = TimeEligibility(
                            status=charge_id_to_time_eligibility[attractor.id].status,
                            reason='Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)',
                            date_will_be_eligible=charge_id_to_time_eligibility[attractor.id].date_will_be_eligible,
                        )
                        charge_id_to_time_eligibility[charge.id] = time_eligibility
        return charge_id_to_time_eligibility

    @staticmethod
    def _categorize_charges(charges):
        dismissals, convictions = [], []
        for charge in charges:
            if charge.dismissed():
                dismissals.append(charge)
            elif charge.convicted():
                convictions.append(charge)
            else:
                raise ValueError("Charge should always convicted or dismissed at this point.")
        return dismissals, convictions

    @staticmethod
    def _most_recent_different_case_dismissal(charge, dismissals):
        different_case_dismissals = [c for c in dismissals if c.case()() != charge.case()()]
        different_case_dismissals.sort(key=lambda charge: charge.date)
        if different_case_dismissals and different_case_dismissals[-1].recent_dismissal():
            return different_case_dismissals[-1]
        else:
            return None

    @staticmethod
    def _most_recent_convictions(recent_convictions):
        recent_convictions.sort(key=lambda charge: charge.disposition.date, reverse=True)
        newer, older = take(2, padnone(recent_convictions))
        if newer and "violation" in newer.level.lower():
            return older
        else:
            return newer

    @staticmethod
    def _calculate_has_subsequent_charge(class_b_felony: Charge, other_charges: List[Charge]) -> bool:
        for other_charge in other_charges:
            if other_charge.dismissed():
                date_of_other_charge = other_charge.date
            else:
                date_of_other_charge = other_charge.disposition.date  # type: ignore

            if date_of_other_charge > class_b_felony.disposition.date:  # type: ignore
                return True
        return False

    @staticmethod
    def _without_skippable_charges(charges: Iterator[Charge]):
        return [charge for charge in charges if charge.disposition and (charge.convicted() or charge.dismissed())]


class ErrorChecker:
    @staticmethod
    def check(record) -> List[str]:
        errors: List[str] = []
        open_cases = [case for case in record.cases if not case.closed()]
        if len(open_cases) > 0:
            case_numbers = ", ".join([f"[{case.case_number}]" for case in open_cases])
            errors += [
                f"All charges are ineligible because there is one or more open case: {case_numbers}. Open cases with valid dispositions are still included in time analysis. Otherwise they are ignored, so time analysis may be inaccurate for other charges."
            ]
        errors += ErrorChecker._build_disposition_errors(record.charges)
        return errors

    @staticmethod
    def _build_disposition_errors(charges: List[Charge]):
        record_errors = []
        cases_with_missing_disposition, cases_with_unrecognized_disposition = ErrorChecker._filter_cases_with_errors(
            charges
        )
        if cases_with_missing_disposition:
            record_errors.append(ErrorChecker._build_missing_disposition_error_message(cases_with_missing_disposition))
        if cases_with_unrecognized_disposition:
            record_errors.append(
                ErrorChecker._build_unrecognized_disposition_error_message(cases_with_unrecognized_disposition)
            )
        return record_errors

    @staticmethod
    def _filter_cases_with_errors(charges: List[Charge]):
        cases_with_missing_disposition: Set[str] = set()
        cases_with_unrecognized_disposition: Set[Tuple[str, str]] = set()
        for charge in charges:
            if charge.blocks_other_charges():
                case_number = f"[{charge.case()().case_number}]"
                if not charge.disposition and charge.case()().closed():
                    cases_with_missing_disposition.add(case_number)
                elif charge.disposition and charge.disposition.status == DispositionStatus.UNRECOGNIZED:
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
