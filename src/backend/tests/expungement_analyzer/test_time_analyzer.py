import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expungement_analyzer.time_analyzer import TimeAnalyzer
from tests.factories.charge import ChargeFactory


class TestSingleChargeAcquittals(unittest.TestCase):
    TEN_YEARS_AGO = (date.today() + relativedelta(years=-10))
    LESS_THAN_THREE_YEARS_AGO = date.today() + relativedelta(years=-3, days=+1)
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3))
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2))

    TEN_YEARS = relativedelta(years=10)

    def setUp(self):
        self.charges = []

    def test_more_than_ten_year_old_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])
        three_yr_mrc = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=three_yr_mrc)
        self.charges.extend([ten_yr_charge, three_yr_mrc])
        time_analyzer.evaluate(self.charges)

        assert ten_yr_charge.expungement_result.time_eligibility is False
        assert ten_yr_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.date_of_eligibility == three_yr_mrc.disposition.date + self.TEN_YEARS

        assert three_yr_mrc.expungement_result.time_eligibility is True
        assert three_yr_mrc.expungement_result.time_eligibility_reason == ''
        assert three_yr_mrc.expungement_result.date_of_eligibility is None

    def test_10_yr_old_conviction_with_less_than_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])
        less_than_three_yr_mrc = ChargeFactory.create(disposition=['Convicted', self.LESS_THAN_THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=less_than_three_yr_mrc)
        self.charges.extend([ten_yr_charge, less_than_three_yr_mrc])
        time_analyzer.evaluate(self.charges)

        assert ten_yr_charge.expungement_result.time_eligibility is False
        assert ten_yr_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.date_of_eligibility == less_than_three_yr_mrc.disposition.date + self.TEN_YEARS

        assert less_than_three_yr_mrc.expungement_result.time_eligibility is False
        assert less_than_three_yr_mrc.expungement_result.time_eligibility_reason == 'Most recent conviction is less than three years old'
        assert less_than_three_yr_mrc.expungement_result.date_of_eligibility == date.today() + relativedelta(days=+1)

    def test_more_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_less_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.LESS_THAN_THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=charge)
        self.charges.append(charge)
        time_analyzer.evaluate(self.charges)

        assert charge.expungement_result.time_eligibility is False
        assert charge.expungement_result.time_eligibility_reason == 'Most recent conviction is less than three years old'
        assert charge.expungement_result.date_of_eligibility == date.today() + relativedelta(days=+1)

    def test_3_yr_old_conviction_2_yr_old_mrc(self):
        three_years_ago_charge = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])
        two_years_ago_charge = ChargeFactory.create(disposition=['Convicted', self.TWO_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=two_years_ago_charge,
                                     second_most_recent_conviction=three_years_ago_charge)
        self.charges.extend([three_years_ago_charge, two_years_ago_charge])
        time_analyzer.evaluate(self.charges)

        assert three_years_ago_charge.expungement_result.time_eligibility is False
        assert three_years_ago_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert three_years_ago_charge.expungement_result.date_of_eligibility == two_years_ago_charge.disposition.date + self.TEN_YEARS

        assert two_years_ago_charge.expungement_result.time_eligibility is False
        assert two_years_ago_charge.expungement_result.time_eligibility_reason == 'Multiple convictions within last ten years'
        assert two_years_ago_charge.expungement_result.date_of_eligibility == three_years_ago_charge.disposition.date + self.TEN_YEARS
