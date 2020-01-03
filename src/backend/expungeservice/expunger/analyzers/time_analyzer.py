from datetime import date
from dateutil.relativedelta import relativedelta

from expungeservice.models.expungement_result import TypeEligibility, ExpungementResult, EligibilityStatus


class TimeAnalyzer:

    TWENTY_YEARS = 20
    TEN_YEARS = 10
    THREE_YEARS = 3

    @staticmethod
    def evaluate(expunger):
        if expunger.most_recent_conviction:
            elig_date = TimeAnalyzer._calc_elig_date(expunger.most_recent_conviction, TimeAnalyzer.TEN_YEARS)
            TimeAnalyzer._mark_as_time_ineligible(expunger.charges, 'Time-ineligible under 137.225(7)(b)', elig_date)
            TimeAnalyzer._check_mrc_time_eligibility(expunger)
        elif expunger.most_recent_dismissal:
            TimeAnalyzer._mark_all_acquittals_ineligible_using_mrd_date(expunger)
            TimeAnalyzer._mark_as_time_eligible(expunger.most_recent_dismissal.case()().charges)
            TimeAnalyzer._mark_as_time_eligible(expunger.convictions)
        else:
            # There is no MRC and no MRD. But the record might still have a single recent violation conviction,
            # Which is subject to the three-year single conviction rule.
            recent_violation_convictions = [
                charge for charge in expunger.charges if charge not in
                    expunger.unknowns +
                    expunger.old_convictions +
                    expunger.acquittals
                    ]

            if len(recent_violation_convictions) == 0:
                pass
            elif len(recent_violation_convictions) == 1:
                recent_violation_conviction = recent_violation_convictions[0]
                three_years_ago = date.today() + relativedelta(years=-3)
                older_than_three_years = recent_violation_conviction.disposition.date <= three_years_ago
                if older_than_three_years:
                    recent_violation_conviction.set_time_eligible()
                else:
                    date_eligible = recent_violation_conviction.disposition.date + relativedelta(years=+3)
                    recent_violation_conviction.set_time_ineligible("Time-ineligible under 137.225(1)(a)", date_eligible)
            else:
                raise ValueError("There is no MRC and no MRD, so the recent known charges should only contain a single violation or nothing.")
            TimeAnalyzer._mark_as_time_eligible(expunger.old_convictions + expunger.acquittals)

        TimeAnalyzer._evaluate_class_b_felonies(expunger)

    @staticmethod
    def _check_mrc_time_eligibility(expunger):
        eligibility_date = TimeAnalyzer._calc_furthest_out_elig_date(expunger)
        if expunger.second_most_recent_conviction:
            expunger.most_recent_conviction.set_time_ineligible('Multiple convictions within last ten years', eligibility_date)
        elif TimeAnalyzer._most_recent_conviction_is_greater_than_three_years_old(expunger):
            expunger.most_recent_conviction.set_time_eligible()
        else:
            expunger.most_recent_conviction.set_time_ineligible('Most recent conviction is less than three years old', eligibility_date)

    @staticmethod
    def _calc_furthest_out_elig_date(expunger):
        if expunger.second_most_recent_conviction:
            date_1 = TimeAnalyzer._calc_elig_date(expunger.second_most_recent_conviction, TimeAnalyzer.TEN_YEARS)
            date_2 = TimeAnalyzer._calc_elig_date(expunger.most_recent_conviction, TimeAnalyzer.THREE_YEARS)
            return max(date_1, date_2)
        else:
            return TimeAnalyzer._calc_elig_date(expunger.most_recent_conviction, TimeAnalyzer.THREE_YEARS)

    @staticmethod
    def _calc_elig_date(charge, years):
        return charge.disposition.date + relativedelta(years=years)

    @staticmethod
    def _most_recent_conviction_is_greater_than_three_years_old(expunger):
        three_years_ago = date.today() + relativedelta(years=-3)
        return expunger.most_recent_conviction.disposition.date <= three_years_ago

    @staticmethod
    def _mark_all_acquittals_ineligible_using_mrd_date(expunger):
        eligibility_date = expunger.most_recent_dismissal.date + relativedelta(years=+TimeAnalyzer.THREE_YEARS)
        for charge in expunger.acquittals:
            charge.set_time_ineligible('Recommend sequential expungement', eligibility_date)

    @staticmethod
    def _calculate_has_subsequent_charge(class_b_felony, charges):
        other_charges = [charge for charge in charges if charge != class_b_felony]
        for other_charge in other_charges:
            if other_charge.acquitted():
                date_of_other_charge = other_charge.date
            else:
                date_of_other_charge = other_charge.disposition.date

            if date_of_other_charge > class_b_felony.disposition.date:
                return True
        return False

    @staticmethod
    def _evaluate_class_b_felonies(expunger):
        for class_b_felony in expunger.class_b_felonies:
            # If the class B felony is acquitted, then we have already handled its time eligibility.
            # If it's convicted, it is subject to these additional rules.
            # If its disposition is unknown, we don't apply any time analysis.
            if class_b_felony.convicted():
                if TimeAnalyzer._calculate_has_subsequent_charge(class_b_felony, expunger.charges):
                    class_b_felony.set_time_ineligible('137.225(5)(a)(A)(ii) - Class B felony can have no subsequent arrests or convictions', None)
                else:
                    eligibility_date = class_b_felony.disposition.date + relativedelta(years=+TimeAnalyzer.TWENTY_YEARS)
                    if eligibility_date > date.today():
                        class_b_felony.set_time_ineligible('137.225(5)(a)(A)(i) - Twenty years from class B felony conviction', eligibility_date)
                    # else do nothing, because the charge has already been set as time eligible by the TimeAnalyzer.

    @staticmethod
    def _mark_as_time_ineligible(charges, reason, eligibility_date):
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    @staticmethod
    def _mark_as_time_eligible(charges):
        for charge in charges:
            charge.set_time_eligible()
