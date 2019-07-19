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
            TimeAnalyzer._mark_all_charges_ineligible_using_mrc_date(expunger, 'Time-ineligible under 137.225(7)(b)',
                                                                     TimeAnalyzer.TEN_YEARS)
            TimeAnalyzer._check_mrc_time_eligibility(expunger)
        elif expunger.most_recent_dismissal and TimeAnalyzer._more_than_one_recent_acquittal_from_another_case(expunger):
            TimeAnalyzer._mark_all_charges_ineligible_using_mrd_date(expunger,
                                                                     'Recommend sequential expungement of arrests')
            TimeAnalyzer._mark_all_mrd_case_related_charges_eligible(expunger)
        else:
            TimeAnalyzer._mark_all_charges_eligible(expunger)

        TimeAnalyzer._evaluate_class_b_felonies(expunger)

    @staticmethod
    def _mark_all_charges_ineligible_using_mrc_date(expunger, reason, years):
        eligibility_date = expunger.most_recent_conviction.disposition.date + relativedelta(years=years)
        for charge in expunger.charges:
            charge.set_time_ineligible(reason, eligibility_date)

    @staticmethod
    def _check_mrc_time_eligibility(expunger):
        if expunger.second_most_recent_conviction:
            eligibility_date = expunger.second_most_recent_conviction.disposition.date + relativedelta(
                years=TimeAnalyzer.TEN_YEARS)
            expunger.most_recent_conviction.set_time_ineligible('Multiple convictions within last ten years',
                                                                eligibility_date)
        elif TimeAnalyzer._most_recent_conviction_is_greater_than_three_years_old(expunger):
            expunger.most_recent_conviction.set_time_eligible()
        else:
            eligibility_date = expunger.most_recent_conviction.disposition.date + relativedelta(
                years=TimeAnalyzer.THREE_YEARS)
            expunger.most_recent_conviction.set_time_ineligible('Most recent conviction is less than three years old',
                                                                eligibility_date)

    @staticmethod
    def _most_recent_conviction_is_greater_than_three_years_old(expunger):
        three_years_ago = date.today() + relativedelta(years=-3)
        return expunger.most_recent_conviction.disposition.date <= three_years_ago

    @staticmethod
    def _more_than_one_recent_acquittal_from_another_case(expunger):
        return expunger.num_acquittals - len(expunger.most_recent_dismissal.case()().charges) > 0

    @staticmethod
    def _mark_all_charges_ineligible_using_mrd_date(expunger, reason):
        eligibility_date = expunger.most_recent_dismissal.date + relativedelta(years=+TimeAnalyzer.THREE_YEARS)
        for charge in expunger.charges:
            charge.set_time_ineligible(reason, eligibility_date)

    @staticmethod
    def _mark_all_mrd_case_related_charges_eligible(expunger):
        for charge in expunger.most_recent_dismissal.case()().charges:
            charge.set_time_eligible('Recommend sequential expungement of arrests')

    @staticmethod
    def _evaluate_class_b_felonies(expunger):
        if expunger.most_recent_charge and expunger.most_recent_charge.disposition.date > TimeAnalyzer.TWENTY_YEARS_AGO:
            for charge in expunger.class_b_felonies:
                charge.set_time_ineligible('Time-ineligible under 137.225(5)(a)(A)(i)',
                                           expunger.most_recent_charge.disposition.date + relativedelta(
                                               years=TimeAnalyzer.TWENTY_YEARS))

    @staticmethod
    def _mark_all_charges_eligible(expunger):
        for charge in expunger.charges:
            charge.set_time_eligible()
