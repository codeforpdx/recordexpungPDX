import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expungement_analyzer.time_analyzer import TimeAnalyzer
from tests.factories.charge import ChargeFactory


class TestSingleChargeAcquittals(unittest.TestCase):

    def setUp(self):
        self.charges = []

    def test_more_than_ten_year_old_conviction(self):
        ten_years_ago = (date.today() + relativedelta(years=-10))
        charge = ChargeFactory.create(disposition=['Convicted', ten_years_ago])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_more_than_three_year_rule_conviction(self):
        more_than_three_year_old_conviction = (date.today() + relativedelta(years=-3))
        charge = ChargeFactory.create(disposition=['Convicted', more_than_three_year_old_conviction])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_less_than_three_year_rule_conviction(self):
        less_than_three_year_old_conviction= (date.today() + relativedelta(years=-3, days=+1))
        charge = ChargeFactory.create(disposition=['Convicted', less_than_three_year_old_conviction])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is False
        assert charge.expungement_result.time_eligibility_reason == 'Most recent conviction is less than three years old'
        assert charge.expungement_result.date_of_eligibility == date.today() + relativedelta(days=+1)
