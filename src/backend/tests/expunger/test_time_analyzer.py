import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestSingleChargeAcquittals(unittest.TestCase):
    TEN_YEARS_AGO = (date.today() + relativedelta(years=-10))
    SEVEN_YEARS_AGO = (date.today() + relativedelta(years=-7))
    FIVE_YEARS_AGO = (date.today() + relativedelta(years=-5))
    LESS_THAN_THREE_YEARS_AGO = date.today() + relativedelta(years=-3, days=+1)
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3))
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2))

    ONE_YEARS_FROM_NOW = date.today() + relativedelta(years=+1)
    TEN_YEARS = relativedelta(years=10)

    def setUp(self):
        self.charges = []

    def test_more_than_ten_year_old_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])

        time_analyzer = TimeAnalyzer()
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

    def test_7_yr_old_conviction_5_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(disposition=['Convicted', self.SEVEN_YEARS_AGO])
        five_year_ago_charge = ChargeFactory.create(disposition=['Convicted', self.FIVE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_conviction=five_year_ago_charge,
                                     second_most_recent_conviction=seven_year_ago_charge)
        self.charges.extend([five_year_ago_charge, seven_year_ago_charge])
        time_analyzer.evaluate(self.charges)

        assert seven_year_ago_charge.expungement_result.time_eligibility is False
        assert seven_year_ago_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert seven_year_ago_charge.expungement_result.date_of_eligibility == five_year_ago_charge.disposition.date + self.TEN_YEARS

        assert five_year_ago_charge.expungement_result.time_eligibility is False
        assert five_year_ago_charge.expungement_result.time_eligibility_reason == 'Multiple convictions within last ten years'
        assert five_year_ago_charge.expungement_result.date_of_eligibility == seven_year_ago_charge.disposition.date + self.TEN_YEARS

    def test_less_than_3yr_old_acquittal(self):
        less_than_3yr_acquittal = ChargeFactory.create(disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_dismissal=less_than_3yr_acquittal)
        self.charges.append(less_than_3yr_acquittal)
        time_analyzer.evaluate(self.charges)

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == ''
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility is None

    def test_multiple_acquittals_with_2yr_old_acquittal(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case, date=self.TWO_YEARS_AGO.strftime('%m/%d/%Y'), disposition=['Dismissed', self.TWO_YEARS_AGO])
        case.charges = [two_year_acquittal]

        less_than_3yr_acquittal = ChargeFactory.create(disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])

        time_analyzer = TimeAnalyzer(most_recent_dismissal=two_year_acquittal, num_acquittals=2)
        self.charges.extend([two_year_acquittal, less_than_3yr_acquittal])
        time_analyzer.evaluate(self.charges)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is False
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == self.ONE_YEARS_FROM_NOW

    def test_multiple_acquittals_belonging_to_same_case(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case,
                                                  date=self.TWO_YEARS_AGO.strftime('%m/%d/%Y'),
                                                  disposition=['Dismissed', self.TWO_YEARS_AGO])
        less_than_3yr_acquittal = ChargeFactory.create(case=case, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case.charges=[two_year_acquittal, less_than_3yr_acquittal]

        time_analyzer = TimeAnalyzer(most_recent_dismissal=two_year_acquittal, num_acquittals=2)
        self.charges.extend([two_year_acquittal, less_than_3yr_acquittal])
        time_analyzer.evaluate(self.charges)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == ''
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == ''
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == None

    def test_multiple_case_recent_acquittals(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case,
                                                  date=self.TWO_YEARS_AGO.strftime('%m/%d/%Y'),
                                                  disposition=['Dismissed', self.TWO_YEARS_AGO])
        less_than_3yr_acquittal = ChargeFactory.create(case=case, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case.charges=[two_year_acquittal, less_than_3yr_acquittal]

        case_2 = CaseFactory.create()
        less_than_3yr_acquittal_2 = ChargeFactory.create(case=case_2, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case_2.charges=[less_than_3yr_acquittal_2]

        time_analyzer = TimeAnalyzer(most_recent_dismissal=two_year_acquittal, num_acquittals=3)
        self.charges.extend([two_year_acquittal, less_than_3yr_acquittal, less_than_3yr_acquittal_2])
        time_analyzer.evaluate(self.charges)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == None

        assert less_than_3yr_acquittal_2.expungement_result.time_eligibility is False
        assert less_than_3yr_acquittal_2.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal_2.expungement_result.date_of_eligibility == self.ONE_YEARS_FROM_NOW
