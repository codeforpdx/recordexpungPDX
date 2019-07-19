import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.expunger_factory import ExpungerFactory


class TestSingleChargeAcquittals(unittest.TestCase):
    TWENTY_YEARS_AGO = (date.today() + relativedelta(years=-20)).strftime('%m/%d/%Y')
    LESS_THAN_TWENTY_YEARS_AGO = (date.today() + relativedelta(years=-20, days=+1)).strftime('%m/%d/%Y')
    TEN_YEARS_AGO = (date.today() + relativedelta(years=-10)).strftime('%m/%d/%Y')
    SEVEN_YEARS_AGO = (date.today() + relativedelta(years=-7)).strftime('%m/%d/%Y')
    FIVE_YEARS_AGO = (date.today() + relativedelta(years=-5)).strftime('%m/%d/%Y')
    LESS_THAN_THREE_YEARS_AGO = (date.today() + relativedelta(years=-3, days=+1)).strftime('%m/%d/%Y')
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3)).strftime('%m/%d/%Y')
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2)).strftime('%m/%d/%Y')
    TOMORROW = date.today() + relativedelta(days=+1)

    ONE_YEARS_FROM_NOW = date.today() + relativedelta(years=+1)
    TEN_YEARS = relativedelta(years=10)

    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def test_more_than_ten_year_old_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])

        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])
        three_yr_mrc = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = three_yr_mrc
        self.expunger.charges = [ten_yr_charge, three_yr_mrc]
        TimeAnalyzer.evaluate(self.expunger)

        assert ten_yr_charge.expungement_result.time_eligibility is False
        assert ten_yr_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.date_of_eligibility == three_yr_mrc.disposition.date + self.TEN_YEARS

        assert three_yr_mrc.expungement_result.time_eligibility is True
        assert three_yr_mrc.expungement_result.time_eligibility_reason == ''
        assert three_yr_mrc.expungement_result.date_of_eligibility is None

    def test_10_yr_old_conviction_with_less_than_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', self.TEN_YEARS_AGO])
        less_than_three_yr_mrc = ChargeFactory.create(disposition=['Convicted', self.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = less_than_three_yr_mrc
        self.expunger.charges = [ten_yr_charge, less_than_three_yr_mrc]
        TimeAnalyzer.evaluate(self.expunger)

        assert ten_yr_charge.expungement_result.time_eligibility is False
        assert ten_yr_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.date_of_eligibility == less_than_three_yr_mrc.disposition.date + self.TEN_YEARS

        assert less_than_three_yr_mrc.expungement_result.time_eligibility is False
        assert less_than_three_yr_mrc.expungement_result.time_eligibility_reason == 'Most recent conviction is less than three years old'
        assert less_than_three_yr_mrc.expungement_result.date_of_eligibility == date.today() + relativedelta(days=+1)

    def test_more_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = charge
        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_less_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', self.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = charge
        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility is False
        assert charge.expungement_result.time_eligibility_reason == 'Most recent conviction is less than three years old'
        assert charge.expungement_result.date_of_eligibility == date.today() + relativedelta(days=+1)

    def test_3_yr_old_conviction_2_yr_old_mrc(self):
        three_years_ago_charge = ChargeFactory.create(disposition=['Convicted', self.THREE_YEARS_AGO])
        two_years_ago_charge = ChargeFactory.create(disposition=['Convicted', self.TWO_YEARS_AGO])

        self.expunger.most_recent_conviction = two_years_ago_charge
        self.expunger.second_most_recent_conviction = three_years_ago_charge
        self.expunger.charges = [three_years_ago_charge, two_years_ago_charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert three_years_ago_charge.expungement_result.time_eligibility is False
        assert three_years_ago_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert three_years_ago_charge.expungement_result.date_of_eligibility == two_years_ago_charge.disposition.date + self.TEN_YEARS

        assert two_years_ago_charge.expungement_result.time_eligibility is False
        assert two_years_ago_charge.expungement_result.time_eligibility_reason == 'Multiple convictions within last ten years'
        assert two_years_ago_charge.expungement_result.date_of_eligibility == three_years_ago_charge.disposition.date + self.TEN_YEARS

    def test_7_yr_old_conviction_5_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(disposition=['Convicted', self.SEVEN_YEARS_AGO])
        five_year_ago_charge = ChargeFactory.create(disposition=['Convicted', self.FIVE_YEARS_AGO])

        self.expunger.most_recent_conviction = five_year_ago_charge
        self.expunger.second_most_recent_conviction = seven_year_ago_charge
        self.expunger.charges = [five_year_ago_charge, seven_year_ago_charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert seven_year_ago_charge.expungement_result.time_eligibility is False
        assert seven_year_ago_charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(7)(b)'
        assert seven_year_ago_charge.expungement_result.date_of_eligibility == five_year_ago_charge.disposition.date + self.TEN_YEARS

        assert five_year_ago_charge.expungement_result.time_eligibility is False
        assert five_year_ago_charge.expungement_result.time_eligibility_reason == 'Multiple convictions within last ten years'
        assert five_year_ago_charge.expungement_result.date_of_eligibility == seven_year_ago_charge.disposition.date + self.TEN_YEARS

    def test_less_than_3yr_old_acquittal(self):
        less_than_3yr_acquittal = ChargeFactory.create(disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_dismissal = less_than_3yr_acquittal
        self.expunger.charges = [less_than_3yr_acquittal]
        TimeAnalyzer.evaluate(self.expunger)

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == ''
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility is None

    def test_multiple_acquittals_with_2yr_old_acquittal(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case, date=self.TWO_YEARS_AGO, disposition=['Dismissed', self.TWO_YEARS_AGO])
        case.charges = [two_year_acquittal]

        less_than_3yr_acquittal = ChargeFactory.create(disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_dismissal = two_year_acquittal
        self.expunger.num_acquittals = 2

        self.expunger.charges = [two_year_acquittal, less_than_3yr_acquittal]
        TimeAnalyzer.evaluate(self.expunger)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is False
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == self.ONE_YEARS_FROM_NOW

    def test_multiple_acquittals_belonging_to_same_case(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case,
                                                  date=self.TWO_YEARS_AGO,
                                                  disposition=['Dismissed', self.TWO_YEARS_AGO])
        less_than_3yr_acquittal = ChargeFactory.create(case=case, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case.charges = [two_year_acquittal, less_than_3yr_acquittal]

        self.expunger.most_recent_dismissal = two_year_acquittal
        self.expunger.num_acquittals = 2

        self.expunger.charges = [two_year_acquittal, less_than_3yr_acquittal]
        TimeAnalyzer.evaluate(self.expunger)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == ''
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == ''
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == None

    def test_multiple_case_recent_acquittals(self):
        case = CaseFactory.create()
        two_year_acquittal = ChargeFactory.create(case=case,
                                                  date=self.TWO_YEARS_AGO,
                                                  disposition=['Dismissed', self.TWO_YEARS_AGO])
        less_than_3yr_acquittal = ChargeFactory.create(case=case, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case.charges=[two_year_acquittal, less_than_3yr_acquittal]

        case_2 = CaseFactory.create()
        less_than_3yr_acquittal_2 = ChargeFactory.create(case=case_2, disposition=['Dismissed', self.LESS_THAN_THREE_YEARS_AGO])
        case_2.charges = [less_than_3yr_acquittal_2]

        self.expunger.most_recent_dismissal = two_year_acquittal
        self.expunger.num_acquittals = 3

        self.expunger.charges = [two_year_acquittal, less_than_3yr_acquittal, less_than_3yr_acquittal_2]
        TimeAnalyzer.evaluate(self.expunger)

        assert two_year_acquittal.expungement_result.time_eligibility is True
        assert two_year_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert two_year_acquittal.expungement_result.date_of_eligibility is None

        assert less_than_3yr_acquittal.expungement_result.time_eligibility is True
        assert less_than_3yr_acquittal.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal.expungement_result.date_of_eligibility == None

        assert less_than_3yr_acquittal_2.expungement_result.time_eligibility is False
        assert less_than_3yr_acquittal_2.expungement_result.time_eligibility_reason == 'Recommend sequential expungement of arrests'
        assert less_than_3yr_acquittal_2.expungement_result.date_of_eligibility == self.ONE_YEARS_FROM_NOW

    def test_felony_class_b_greater_than_20yrs(self):
        charge = ChargeFactory.create(name='Aggravated theft in the first degree',
                                      statute='164.057',
                                      level='Felony Class B',
                                      date=self.TWENTY_YEARS_AGO,
                                      disposition=['Convicted', self.TWENTY_YEARS_AGO])

        self.expunger.class_b_felonies = [charge]
        self.expunger.most_recent_charge = charge

        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility is True
        assert charge.expungement_result.time_eligibility_reason == ''
        assert charge.expungement_result.date_of_eligibility is None

    def test_felony_class_b_less_than_20yrs(self):
        charge = ChargeFactory.create(name='Aggravated theft in the first degree',
                                      statute='164.057',
                                      level='Felony Class B',
                                      date=self.LESS_THAN_TWENTY_YEARS_AGO,
                                      disposition=['Convicted', self.LESS_THAN_TWENTY_YEARS_AGO])

        self.expunger.class_b_felonies = [charge]
        self.expunger.most_recent_charge = charge

        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility is False
        assert charge.expungement_result.time_eligibility_reason == 'Time-ineligible under 137.225(5)(a)(A)(i)'
        assert charge.expungement_result.date_of_eligibility == self.TOMORROW
