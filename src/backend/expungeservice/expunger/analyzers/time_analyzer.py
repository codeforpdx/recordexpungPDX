from datetime import date
from typing import List

from dateutil.relativedelta import relativedelta

from expungeservice.expunger.charges_summarizer import ChargesWithSummary
from expungeservice.models.charge import Charge


class TimeAnalyzer:
    TWENTY_YEARS = 20
    TEN_YEARS = 10
    THREE_YEARS = 3

    # TODO: Change to `def evaluate(record: Record, charges_with_summary: ChargesWithSummary) -> RecordWithAnalysis:`
    @staticmethod
    def evaluate(charges_with_summary: ChargesWithSummary):
        if charges_with_summary.most_recent_conviction:
            elig_date = TimeAnalyzer._calc_elig_date(charges_with_summary.most_recent_conviction, TimeAnalyzer.TEN_YEARS)
            TimeAnalyzer._mark_as_time_ineligible(charges_with_summary.charges, 'Time-ineligible under 137.225(7)(b)', elig_date)
            TimeAnalyzer._check_mrc_time_eligibility(charges_with_summary)
        elif charges_with_summary.most_recent_dismissal:
            TimeAnalyzer._mark_all_acquittals_ineligible_using_mrd_date(charges_with_summary)
            TimeAnalyzer._mark_as_time_eligible(charges_with_summary.most_recent_dismissal.case()().charges)
            TimeAnalyzer._mark_as_time_eligible(charges_with_summary.convictions)
        else:
            # There is no MRC and no MRD. But the record might still have a single recent violation conviction,
            # Which is subject to the three-year single conviction rule.
            recent_violation_convictions = [
                charge for charge in charges_with_summary.charges if charge not in
                                                                     charges_with_summary.unknowns +
                                                                     charges_with_summary.old_convictions +
                                                                     charges_with_summary.acquittals
                    ]

            if len(recent_violation_convictions) == 0:
                pass
            elif len(recent_violation_convictions) == 1:
                recent_violation_conviction = recent_violation_convictions[0]
                three_years_ago = date.today() + relativedelta(years=-3)
                older_than_three_years = recent_violation_conviction.disposition.date <= three_years_ago # type: ignore
                if older_than_three_years:
                    recent_violation_conviction.set_time_eligible()
                else:
                    date_eligible = recent_violation_conviction.disposition.date + relativedelta(years=+3) # type: ignore
                    recent_violation_conviction.set_time_ineligible("Time-ineligible under 137.225(1)(a)", date_eligible)
            else:
                raise ValueError("There is no MRC and no MRD, so the recent known charges should only contain a single violation or nothing.")
            TimeAnalyzer._mark_as_time_eligible(charges_with_summary.old_convictions + charges_with_summary.acquittals)

        TimeAnalyzer._evaluate_class_b_felonies(charges_with_summary)

    @staticmethod
    def _check_mrc_time_eligibility(charges: ChargesWithSummary):
        eligibility_date = TimeAnalyzer._calc_furthest_out_elig_date(charges)
        if charges.second_most_recent_conviction:
            charges.most_recent_conviction.set_time_ineligible('Multiple convictions within last ten years', eligibility_date) # type: ignore
        elif TimeAnalyzer._most_recent_conviction_is_greater_than_three_years_old(charges):
            charges.most_recent_conviction.set_time_eligible() # type: ignore
        else:
            charges.most_recent_conviction.set_time_ineligible('Most recent conviction is less than three years old', eligibility_date) # type: ignore

    @staticmethod
    def _calc_furthest_out_elig_date(charges_with_summary: ChargesWithSummary):
        if charges_with_summary.second_most_recent_conviction:
            date_1 = TimeAnalyzer._calc_elig_date(charges_with_summary.second_most_recent_conviction, TimeAnalyzer.TEN_YEARS)
            date_2 = TimeAnalyzer._calc_elig_date(charges_with_summary.most_recent_conviction, TimeAnalyzer.THREE_YEARS) # type: ignore
            return max(date_1, date_2)
        else:
            return TimeAnalyzer._calc_elig_date(charges_with_summary.most_recent_conviction, TimeAnalyzer.THREE_YEARS) # type: ignore

    @staticmethod
    def _calc_elig_date(charge: Charge, years: int) -> date:
        return charge.disposition.date + relativedelta(years=years) # type: ignore

    @staticmethod
    def _most_recent_conviction_is_greater_than_three_years_old(charges: ChargesWithSummary):
        three_years_ago = date.today() + relativedelta(years=-3)
        return charges.most_recent_conviction.disposition.date <= three_years_ago # type: ignore

    @staticmethod
    def _mark_all_acquittals_ineligible_using_mrd_date(charges_with_summary: ChargesWithSummary):
        eligibility_date = charges_with_summary.most_recent_dismissal.date + relativedelta(years=+TimeAnalyzer.THREE_YEARS) # type: ignore
        for charge in charges_with_summary.acquittals:
            charge.set_time_ineligible('Recommend sequential expungement', eligibility_date)

    @staticmethod
    def _calculate_has_subsequent_charge(class_b_felony: Charge, charges: List[Charge]) -> bool:
        other_charges = [charge for charge in charges if charge != class_b_felony]
        for other_charge in other_charges:
            if other_charge.acquitted():
                date_of_other_charge = other_charge.date
            else:
                date_of_other_charge = other_charge.disposition.date # type: ignore

            if date_of_other_charge > class_b_felony.disposition.date: # type: ignore
                return True
        return False

    @staticmethod
    def _evaluate_class_b_felonies(charges_with_summary: ChargesWithSummary):
        for class_b_felony in charges_with_summary.class_b_felonies:
            # If the class B felony is acquitted, then we have already handled its time eligibility.
            # If it's convicted, it is subject to these additional rules.
            # If its disposition is unknown, we don't apply any time analysis.
            if class_b_felony.convicted():
                if TimeAnalyzer._calculate_has_subsequent_charge(class_b_felony, charges_with_summary.charges):
                    class_b_felony.set_time_ineligible('137.225(5)(a)(A)(ii) - Class B felony can have no subsequent arrests or convictions', None)
                else:
                    eligibility_date = class_b_felony.disposition.date + relativedelta(years=+TimeAnalyzer.TWENTY_YEARS) # type: ignore
                    if eligibility_date > date.today():
                        class_b_felony.set_time_ineligible('137.225(5)(a)(A)(i) - Twenty years from class B felony conviction', eligibility_date)
                    # else do nothing, because the charge has already been set as time eligible by the TimeAnalyzer.

    @staticmethod
    def _mark_as_time_ineligible(charges: List[Charge], reason: str, eligibility_date: date):
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    @staticmethod
    def _mark_as_time_eligible(charges: List[Charge]):
        for charge in charges:
            charge.set_time_eligible()
