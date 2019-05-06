from datetime import date
from dateutil.relativedelta import relativedelta


class TimeAnalyzer:

    THREE_YEARS = 3
    TEN_YEARS = 10

    def __init__(self, most_recent_conviction=None, second_most_recent_conviction=None, most_recent_dismissal=None, num_acquittals=0):
        """

        :param most_recent_conviction: Most recent conviction if one exists from within the last ten years
        :param second_most_recent_conviction: Second most recent conviction if one exists from within the last ten years
        :param most_recent_dismissal: Most recent dismissal if one exists from within the last three years
        :param num_acquittals: Number of acquittals within the last three years
        """
        self._most_recent_conviction = most_recent_conviction
        self._second_most_recent_conviction = second_most_recent_conviction
        self._most_recent_dismissal = most_recent_dismissal
        self._num_acquittals = num_acquittals

    def evaluate(self, charges):
        if self._most_recent_conviction:
            self._mark_all_charges_ineligible_using_mrc_date(charges, 'Time-ineligible under 137.225(7)(b)', self.TEN_YEARS)
            self._check_mrc_time_eligibility()
        elif self._most_recent_dismissal and self._more_than_one_recent_acquittal_from_another_case():
            self._mark_all_charges_ineligible_using_mrd_date(charges, 'Recommend sequential expungement of arrests')
            self._mark_all_mrd_case_related_charges_eligible()
        else:
            TimeAnalyzer._mark_all_charges_eligible(charges)

    def _mark_all_charges_ineligible_using_mrc_date(self, charges, reason, years):
        eligibility_date = self._most_recent_conviction.disposition.date + relativedelta(years=years)
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    def _check_mrc_time_eligibility(self):
        if self._second_most_recent_conviction:
            eligibility_date = self._second_most_recent_conviction.disposition.date + relativedelta(years=self.TEN_YEARS)
            self._most_recent_conviction.set_time_ineligible('Multiple convictions within last ten years', eligibility_date)
        elif self._most_recent_conviction_is_greater_than_three_years_old():
            self._most_recent_conviction.set_time_eligible()
        else:
            eligibility_date = self._most_recent_conviction.disposition.date + relativedelta(years=self.THREE_YEARS)
            self._most_recent_conviction.set_time_ineligible('Most recent conviction is less than three years old', eligibility_date)

    def _most_recent_conviction_is_greater_than_three_years_old(self):
        three_years_ago = date.today() + relativedelta(years=-3)
        return self._most_recent_conviction.disposition.date <= three_years_ago

    def _more_than_one_recent_acquittal_from_another_case(self):
        return self._num_acquittals - len(self._most_recent_dismissal.case()().charges) > 0

    def _mark_all_charges_ineligible_using_mrd_date(self, charges, reason):
        eligibility_date = self._most_recent_dismissal.date + relativedelta(years=+self.THREE_YEARS)
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    def _mark_all_mrd_case_related_charges_eligible(self):
        for charge in self._most_recent_dismissal.case()().charges:
            charge.set_time_eligible('Recommend sequential expungement of arrests')

    @staticmethod
    def _mark_all_charges_eligible(charges):
        for charge in charges:
            charge.set_time_eligible()
