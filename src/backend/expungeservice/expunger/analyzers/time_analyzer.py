from datetime import date
from dateutil.relativedelta import relativedelta


class TimeAnalyzer:

    TWENTY_YEARS_AGO = date.today() + relativedelta(years=-20)
    TWENTY_YEARS = 20
    TEN_YEARS = 10
    THREE_YEARS = 3

    @staticmethod
    def evaluate(expunger):
        if expunger.most_recent_conviction:
            elig_date = TimeAnalyzer._calc_elig_date(expunger.most_recent_conviction, TimeAnalyzer.TEN_YEARS)
            TimeAnalyzer._mark_as_time_ineligible(expunger.charges, 'Time-ineligible under 137.225(7)(b)', elig_date)
            TimeAnalyzer._check_mrc_time_eligibility(expunger)
            TimeAnalyzer._set_arrests_as_eligible(expunger)
        elif expunger.most_recent_dismissal:
            TimeAnalyzer._mark_all_acquittals_ineligible_using_mrd_date(expunger)
            TimeAnalyzer._mark_as_time_eligible(expunger.most_recent_dismissal.case()().charges)
            TimeAnalyzer._mark_as_time_eligible(expunger.convictions)
        else:
            TimeAnalyzer._mark_as_time_eligible(expunger.charges)

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
    def _evaluate_class_b_felonies(expunger):
        if expunger.most_recent_charge and expunger.most_recent_charge.disposition.date > TimeAnalyzer.TWENTY_YEARS_AGO:
            for charge in expunger.class_b_felonies:
                charge.set_time_ineligible('Time-ineligible under 137.225(5)(a)(A)(i)',
                                           expunger.most_recent_charge.disposition.date + relativedelta(
                                               years=TimeAnalyzer.TWENTY_YEARS))

    @staticmethod
    def _mark_as_time_ineligible(charges, reason, eligibility_date):
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    @staticmethod
    def _set_arrests_as_eligible(expunger):
        if expunger.most_recent_conviction.expungement_result.time_eligibility.status:
        # if len(expunger.charges) > 2:
            arrest_dispositions = {'Dismissed', 'Acquitted', 'Dismissal', 'No Complaint'}
            mrc = expunger.most_recent_conviction
            non_mrc_charges = [x for x in expunger.charges if x != mrc]
            non_mrc_rulings = {x.disposition.ruling for x in non_mrc_charges}
            are_all_arrests = non_mrc_rulings.issubset(arrest_dispositions)
            if are_all_arrests:
                for charge in non_mrc_charges:
                    charge.set_time_eligible()
                # import pdb; pdb.set_trace()
            # If all non-mrc are arrests
            # Then make them all time-eligible


    @staticmethod
    def _mark_as_time_eligible(charges):
        for charge in charges:
            charge.set_time_eligible()
