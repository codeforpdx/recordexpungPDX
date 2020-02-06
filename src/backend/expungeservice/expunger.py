from datetime import date
from typing import Set, List, Iterator, Tuple

from dateutil.relativedelta import relativedelta
from more_itertools import flatten, padnone, take

from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.record import Record


class Expunger:
    def __init__(self, record: Record):
        self.record = record
        self.analyzable_charges = Expunger._without_skippable_charges(self.record.charges)

    def run(self) -> bool:
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        open_cases = [case for case in self.record.cases if not case.closed()]
        if len(open_cases) > 0:
            case_numbers = ",".join([case.case_number for case in open_cases])
            self.record.errors += [
                f"All charges are ineligible because there is one or more open case: {case_numbers}. Open cases with valid dispositions are still included in time analysis. Otherwise they are ignored, so time analysis may be inaccurate for other charges."
            ]
        self.record.errors += self._build_disposition_errors(self.record.charges)
        for charge in self.analyzable_charges:
            eligibility_dates: List[Tuple[date, str]] = []
            other_charges = [c for c in self.analyzable_charges if c != charge and not c.skip_analysis()]
            dismissals, convictions = Expunger._categorize_charges(other_charges)
            most_recent_blocking_dismissal = Expunger._most_recent_different_case_dismissal(charge, dismissals)
            most_recent_blocking_conviction = Expunger._most_recent_convictions(convictions)

            if charge.convicted():
                eligibility_dates.append(
                    (charge.disposition.date + relativedelta(years=3), "Time-ineligible under 137.225(1)(a)")
                )
            elif charge.acquitted():
                eligibility_dates.append((charge.disposition.date, "Time eligible under 137.225(1)(b)"))
            else:
                raise ValueError("Charge should always convicted or acquitted at this point.")

            if charge.expungement_result.type_eligibility.status == EligibilityStatus.INELIGIBLE:
                eligibility_dates.append((date.max, "Never. Type ineligible charges are always time ineligible."))

            if charge.disposition.status == DispositionStatus.NO_COMPLAINT:
                eligibility_dates.append(
                    (charge.disposition.date + relativedelta(years=1), "Time-ineligible under 137.225(1)(b)")
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
                eligibility_dates.append(
                    (
                        most_recent_blocking_conviction.disposition.date + relativedelta(years=10),
                        "Time-ineligible under 137.225(7)(b)",
                    )
                )

            if charge.acquitted() and most_recent_blocking_dismissal:
                eligibility_dates.append(
                    (most_recent_blocking_dismissal.date + relativedelta(years=3), "Recommend sequential expungement")
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
                    eligibility_dates.append((charge.disposition.date + relativedelta(years=20), "137.225(5)(a)(A)(i) - Twenty years from class B felony conviction"))  # type: ignore

            charge.set_time_eligibility(eligibility_dates)
        for case in self.record.cases:
            convictions_in_case = [charge for charge in case.charges if charge.convicted()]
            if len(convictions_in_case) == 1:
                for charge in case.charges:
                    charge.expungement_result.time_eligibility = convictions_in_case[
                        0
                    ].expungement_result.time_eligibility  # TODO: Feels dangerous; clean up
        return len(open_cases) == 0

    @staticmethod
    def _categorize_charges(charges):
        acquittals, convictions = [], []
        for charge in charges:
            if charge.acquitted():
                acquittals.append(charge)
            elif charge.convicted():
                convictions.append(charge)
            else:
                raise ValueError("Charge should always convicted or acquitted at this point.")
        return acquittals, convictions

    @staticmethod
    def _most_recent_different_case_dismissal(charge, acquittals):
        different_case_acquittals = [c for c in acquittals if c.case()() != charge.case()()]
        different_case_acquittals.sort(key=lambda charge: charge.date)
        if different_case_acquittals and different_case_acquittals[-1].recent_acquittal():
            return different_case_acquittals[-1]
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
            if other_charge.acquitted():
                date_of_other_charge = other_charge.date
            else:
                date_of_other_charge = other_charge.disposition.date  # type: ignore

            if date_of_other_charge > class_b_felony.disposition.date:  # type: ignore
                return True
        return False

    @staticmethod
    def _without_skippable_charges(charges: Iterator[Charge]):
        return [charge for charge in charges if charge.disposition and (charge.convicted() or charge.acquitted())]

    @staticmethod
    def _build_disposition_errors(charges: List[Charge]):
        record_errors = []
        cases_with_missing_disposition, cases_with_unrecognized_disposition = Expunger._filter_cases_with_errors(
            charges
        )
        if cases_with_missing_disposition:
            record_errors.append(Expunger._build_missing_disposition_error_message(cases_with_missing_disposition))
        if cases_with_unrecognized_disposition:
            record_errors.append(
                Expunger._build_unrecognized_disposition_error_message(cases_with_unrecognized_disposition)
            )
        return record_errors

    @staticmethod
    def _filter_cases_with_errors(charges: List[Charge]):
        cases_with_missing_disposition: Set[str] = set()
        cases_with_unrecognized_disposition: Set[Tuple[str, str]] = set()
        for charge in charges:
            if not charge.skip_analysis():
                case_number = charge.case()().case_number
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
