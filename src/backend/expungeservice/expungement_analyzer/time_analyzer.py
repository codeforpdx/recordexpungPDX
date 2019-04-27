from datetime import date
from dateutil.relativedelta import relativedelta


class TimeAnalyzer:

    def __init__(self, most_recent_conviction):
        self._most_recent_conviction = most_recent_conviction

    def evaluate(self, charges):
        for charge in charges:
            self._evaluate(charge)

    def _evaluate(self, charge):
        if self._most_recent_conviction_is_greater_than_three_years_old():
            charge.expungement_result.time_eligibility = True
        else:
            charge.expungement_result.time_eligibility = False
            charge.expungement_result.time_eligibility_reason = 'Most recent conviction is less than three years old'
            charge.expungement_result.date_of_eligibility = self._three_years_from_disposition(charge)

    def _most_recent_conviction_is_greater_than_three_years_old(self):
        three_years_ago = date.today() + relativedelta(years=-3)
        return self._most_recent_conviction.disposition.date < three_years_ago

    @staticmethod
    def _three_years_from_disposition(charge):
        return charge.disposition.date + relativedelta(years=+3)
