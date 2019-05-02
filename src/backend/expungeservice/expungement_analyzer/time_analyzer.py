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
        elif self._most_recent_dismissal and self._more_than_one_recent_non_case_related_acquittal():
            self._mark_all_charges_ineligible_using_mrd_date(charges, 'Recommend sequential expungement of arrests')
            self._mark_eligible(self._most_recent_dismissal, 'Recommend sequential expungement of arrests')
        else:
            TimeAnalyzer._mark_all_charges_eligible(charges)

    def _check_mrc_time_eligibility(self):
        if self._most_recent_conviction_is_greater_than_three_years_old():
            self._mark_eligible(self._most_recent_conviction)
        elif self._second_most_recent_conviction:
            self._mark_mrc_ineligible('Multiple convictions within last ten years', self.TEN_YEARS)
        else:
            self._mark_mrc_ineligible('Most recent conviction is less than three years old', self.THREE_YEARS)

    def _mark_eligible(self, charge, reason=''):
        charge.expungement_result.time_eligibility = True
        charge.expungement_result.time_eligibility_reason = reason
        charge.expungement_result.date_of_eligibility = None

    def _most_recent_conviction_is_greater_than_three_years_old(self):
        three_years_ago = date.today() + relativedelta(years=-3)
        return self._most_recent_conviction.disposition.date <= three_years_ago

    def _mark_all_charges_ineligible_using_mrc_date(self, charges, reason, date):
        for charge in charges:
            self._mark_ineligible_by_mrc_disposition_date(charge, reason, date)

    def _mark_all_charges_ineligible_using_mrd_date(self, charges, reason):
        for charge in charges:
            self._mark_ineligible_by_mrd_arrest_date(charge, reason)

    def _mark_ineligible_by_mrc_disposition_date(self, charge, reason, years):
        TimeAnalyzer._mark_eligibleness(charge, False)
        TimeAnalyzer._add_reason(charge, reason)
        TimeAnalyzer._date_of_eligibility(charge, self._most_recent_conviction, years)

    def _mark_ineligible_by_mrd_arrest_date(self, charge, reason):
        TimeAnalyzer._mark_eligibleness(charge, False)
        TimeAnalyzer._add_reason(charge, reason)
        charge.expungement_result.date_of_eligibility = self._most_recent_dismissal.date + relativedelta(years=+3)

    def _mark_mrc_ineligible(self, reason, years):
        TimeAnalyzer._mark_eligibleness(self._most_recent_conviction, False)
        TimeAnalyzer._add_reason(self._most_recent_conviction, reason)
        if self._second_most_recent_conviction:
            TimeAnalyzer._date_of_eligibility(self._most_recent_conviction, self._second_most_recent_conviction, years)
        else:
            TimeAnalyzer._date_of_eligibility(self._most_recent_conviction, self._most_recent_conviction, years)

    def _more_than_one_recent_non_case_related_acquittal(self):
        return self._num_acquittals - len(self._most_recent_dismissal.case()().charges) > 1

    @staticmethod
    def _three_years_from_disposition(charge):
        return charge.disposition.date + relativedelta(years=+3)

    @staticmethod
    def _mark_eligibleness(charge, eligibility):
        charge.expungement_result.time_eligibility = eligibility

    @staticmethod
    def _add_reason(charge, reason):
        charge.expungement_result.time_eligibility_reason = reason

    @staticmethod
    def _date_of_eligibility(charge, mrc, years):
        charge.expungement_result.date_of_eligibility = mrc.disposition.date + relativedelta(years=years)

    @staticmethod
    def _mark_all_charges_eligible(charges):
        for charge in charges:
            TimeAnalyzer._mark_eligibleness(charge, True)
