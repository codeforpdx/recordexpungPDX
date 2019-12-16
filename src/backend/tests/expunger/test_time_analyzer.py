import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from expungeservice.expunger.expunger import Expunger
from expungeservice.models.record import Record
from expungeservice.models.expungement_result import EligibilityStatus
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.expunger_factory import ExpungerFactory
from tests.utilities.time import Time


class TestSingleChargeAcquittals(unittest.TestCase):

    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def test_more_than_ten_year_old_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])

        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == ''
        assert charge.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])
        three_yr_mrc = ChargeFactory.create(disposition=['Convicted', Time.THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = three_yr_mrc
        self.expunger.charges = [ten_yr_charge, three_yr_mrc]
        TimeAnalyzer.evaluate(self.expunger)

        assert ten_yr_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert ten_yr_charge.expungement_result.time_eligibility.reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.time_eligibility.date_will_be_eligible == three_yr_mrc.disposition.date + Time.TEN_YEARS

        assert three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert three_yr_mrc.expungement_result.time_eligibility.reason == ''
        assert three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_10_yr_old_conviction_with_less_than_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])
        less_than_three_yr_mrc = ChargeFactory.create(disposition=['Convicted', Time.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = less_than_three_yr_mrc
        self.expunger.charges = [ten_yr_charge, less_than_three_yr_mrc]
        TimeAnalyzer.evaluate(self.expunger)

        assert ten_yr_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert ten_yr_charge.expungement_result.time_eligibility.reason == 'Time-ineligible under 137.225(7)(b)'
        assert ten_yr_charge.expungement_result.time_eligibility.date_will_be_eligible == less_than_three_yr_mrc.disposition.date + Time.TEN_YEARS

        assert less_than_three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert less_than_three_yr_mrc.expungement_result.time_eligibility.reason == 'Most recent conviction is less than three years old'
        assert less_than_three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_more_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', Time.THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = charge
        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == ''
        assert charge.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_less_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(disposition=['Convicted', Time.LESS_THAN_THREE_YEARS_AGO])

        self.expunger.most_recent_conviction = charge
        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == 'Most recent conviction is less than three years old'
        assert charge.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_time_eligibility_date_is_none_when_type_ineligible(self):
        charge = ChargeFactory.create(name='Assault in the first degree',
                                      statute='163.185',
                                      level='Felony Class A',
                                      date=Time.ONE_YEAR_AGO,
                                      disposition=['Convicted', Time.ONE_YEAR_AGO])

        self.expunger.most_recent_conviction = charge
        self.expunger.charges = [charge]
        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is False
        assert charge.expungement_result.time_eligibility.reason == 'Most recent conviction is less than three years old'
        assert charge.expungement_result.time_eligibility.date_will_be_eligible is None


class TestClassBFelony(unittest.TestCase):

    def create_class_b_felony_charge(self, date, ruling='Convicted'):

        return ChargeFactory.create(name='Aggravated theft in the first degree',
                                      statute='164.057',
                                      level='Felony Class B',
                                      date=date,
                                      disposition=[ruling, date])
    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def test_felony_class_b_greater_than_20yrs(self):

        charge = self.create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
        self.expunger.most_recent_charge = charge
        self.expunger.charges = [charge]
        self.expunger._assign_class_b_felonies()


        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == ''
        assert charge.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_felony_class_b_less_than_20yrs(self):

        charge = self.create_class_b_felony_charge(Time.LESS_THAN_TWENTY_YEARS_AGO)
        self.expunger.most_recent_charge = charge
        self.expunger.charges = [charge]
        self.expunger._assign_class_b_felonies()

        TimeAnalyzer.evaluate(self.expunger)

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == '137.225(5)(a)(A)(i) - Twenty years from class B felony conviction'
        assert charge.expungement_result.time_eligibility.date_will_be_eligible == Time.TOMORROW

    def test_felony_class_b_with_subsequent_conviction(self):

        b_felony_charge = self.create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
        subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])

        self.expunger.charges = [b_felony_charge, subsequent_charge]
        self.expunger._assign_class_b_felonies()

        TimeAnalyzer.evaluate(self.expunger)

        assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert b_felony_charge.expungement_result.time_eligibility == None
        assert b_felony_charge.expungement_result.type_eligibility.reason == (
            "137.225(5)(a)(A)(ii) - Class B felony can have no subsquent arrests or convictions")

    def test_felony_class_b_with_prior_conviction(self):

        b_felony_charge = self.create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
        prior_charge = ChargeFactory.create(disposition=['Convicted', Time.OVER_TWENTY_YEARS_AGO])

        self.expunger.charges = [b_felony_charge, prior_charge]
        self.expunger._assign_class_b_felonies()

        TimeAnalyzer.evaluate(self.expunger)

        assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert b_felony_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'
        assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert b_felony_charge.expungement_result.time_eligibility.reason == ''


    def test_acquitted_felony_class_b_with_subsequent_conviction(self):

        b_felony_charge = self.create_class_b_felony_charge(Time.TWENTY_YEARS_AGO, 'Dismissed')

        subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])

        self.expunger.charges = [b_felony_charge, subsequent_charge]
        self.expunger._assign_class_b_felonies()

        TimeAnalyzer.evaluate(self.expunger)

        assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE

    def test_doubly_eligible_b_felony_gets_normal_eligibility_rule(self):
        #This charge is both List B and also a class B felony. List B classification takes precedence.
        list_b_charge = ChargeFactory.create(name='Assault in the second degree',
                                      statute='163.175',
                                      level='Felony Class B',
                                      date=Time.LESS_THAN_TWENTY_YEARS_AGO,
                                      disposition=['Convicted', Time.LESS_THAN_TWENTY_YEARS_AGO])

        subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])

        self.expunger.charges = [list_b_charge, subsequent_charge]
        self.expunger._assign_class_b_felonies()

        TimeAnalyzer.evaluate(self.expunger)

        assert list_b_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS


class TestDismissalBlock(unittest.TestCase):

    def setUp(self):
        self.case_1 = CaseFactory.create()
        self.case_2 = CaseFactory.create()

        self.recent_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_1, date=Time.TWO_YEARS_AGO)
        self.case_1.charges = [self.recent_dismissal]

    def test_record_with_only_an_mrd_is_time_eligible(self):
        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger.run()

        assert self.recent_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.recent_dismissal.expungement_result.time_eligibility.reason == ''
        assert self.recent_dismissal.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_all_mrd_case_related_dismissals_are_expungeable(self):
        case_related_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_1, date=Time.TWO_YEARS_AGO)
        self.case_1.charges.append(case_related_dismissal)

        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger.run()

        assert self.recent_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.recent_dismissal.expungement_result.time_eligibility.reason == ''
        assert self.recent_dismissal.expungement_result.time_eligibility.date_will_be_eligible is None

        assert case_related_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert case_related_dismissal.expungement_result.time_eligibility.reason == ''
        assert case_related_dismissal.expungement_result.time_eligibility.date_will_be_eligible is None

    def test_mrd_blocks_dismissals_in_unrelated_cases(self):
        unrelated_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_2, date=Time.TEN_YEARS_AGO)
        self.case_2.charges = [unrelated_dismissal]

        record = Record([self.case_1, self.case_2])
        expunger = Expunger(record)
        expunger.run()

        assert unrelated_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert unrelated_dismissal.expungement_result.time_eligibility.reason == 'Recommend sequential expungement'
        assert unrelated_dismissal.expungement_result.time_eligibility.date_will_be_eligible == Time.ONE_YEARS_FROM_NOW

    def test_mrd_does_not_block_convictions(self):
        case = CaseFactory.create()
        convicted_charge = ChargeFactory.create(case=case, date=Time.TWENTY_YEARS_AGO, disposition=['Convicted', Time.TWENTY_YEARS_AGO])
        case.charges = [convicted_charge]

        record = Record([self.case_1, case])
        expunger = Expunger(record)
        expunger.run()

        assert convicted_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert convicted_charge.expungement_result.time_eligibility.reason == ''
        assert convicted_charge.expungement_result.time_eligibility.date_will_be_eligible is None


class TestSecondMRCLogic(unittest.TestCase):

    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def run_expunger(self, mrc, second_mrc):
        self.expunger.most_recent_conviction = mrc
        self.expunger.second_most_recent_conviction = second_mrc
        self.expunger.charges = [mrc, second_mrc]
        TimeAnalyzer.evaluate(self.expunger)

    def test_3_yr_old_conviction_2_yr_old_mrc(self):
        three_years_ago_charge = ChargeFactory.create(disposition=['Convicted', Time.THREE_YEARS_AGO])
        two_years_ago_charge = ChargeFactory.create(disposition=['Convicted', Time.TWO_YEARS_AGO])

        self.run_expunger(two_years_ago_charge, three_years_ago_charge)

        assert three_years_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert three_years_ago_charge.expungement_result.time_eligibility.reason == 'Time-ineligible under 137.225(7)(b)'
        assert three_years_ago_charge.expungement_result.time_eligibility.date_will_be_eligible == two_years_ago_charge.disposition.date + Time.TEN_YEARS

        assert two_years_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert two_years_ago_charge.expungement_result.time_eligibility.reason == 'Multiple convictions within last ten years'
        assert two_years_ago_charge.expungement_result.time_eligibility.date_will_be_eligible == three_years_ago_charge.disposition.date + Time.TEN_YEARS

    def test_7_yr_old_conviction_5_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(disposition=['Convicted', Time.SEVEN_YEARS_AGO])
        five_year_ago_charge = ChargeFactory.create(disposition=['Convicted', Time.FIVE_YEARS_AGO])

        self.run_expunger(five_year_ago_charge, seven_year_ago_charge)

        assert seven_year_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert seven_year_ago_charge.expungement_result.time_eligibility.reason == 'Time-ineligible under 137.225(7)(b)'
        assert seven_year_ago_charge.expungement_result.time_eligibility.date_will_be_eligible == five_year_ago_charge.disposition.date + Time.TEN_YEARS

        assert five_year_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert five_year_ago_charge.expungement_result.time_eligibility.reason == 'Multiple convictions within last ten years'
        assert five_year_ago_charge.expungement_result.time_eligibility.date_will_be_eligible == seven_year_ago_charge.disposition.date + Time.TEN_YEARS

    def test_mrc_is_eligible_in_two_years(self):
        nine_year_old_conviction = ChargeFactory.create(disposition=['Convicted', Time.NINE_YEARS_AGO])
        one_year_old_conviction = ChargeFactory.create(disposition=['Convicted', Time.ONE_YEAR_AGO])
        eligibility_date = one_year_old_conviction.disposition.date + Time.THREE_YEARS

        self.run_expunger(one_year_old_conviction, nine_year_old_conviction)

        assert one_year_old_conviction.expungement_result.time_eligibility.date_will_be_eligible == eligibility_date
