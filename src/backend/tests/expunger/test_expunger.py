import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.expunger import Expunger
from expungeservice.crawler.models.disposition import Disposition
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestExpungementAnalyzerUnitTests(unittest.TestCase):

    TEN_YEARS = (date.today() + relativedelta(years=-10)).strftime('%m/%d/%Y')
    LESS_THAN_TEN_YEARS_AGO = (date.today() + relativedelta(years=-10, days=+1)).strftime('%m/%d/%Y')
    LESS_THAN_THREE_YEARS_AGO = (date.today() + relativedelta(years=-3, days=+1)).strftime('%m/%d/%Y')
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3)).strftime('%m/%d/%Y')
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2)).strftime('%m/%d/%Y')
    ONE_YEAR_AGO = (date.today() + relativedelta(years=-1)).strftime('%m/%d/%Y')

    def test_expunger_sets_most_recent_dismissal_when_charge_is_less_than_3yrs(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=self.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [mrd_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_dismissal is mrd_charge

    def test_expunger_does_not_set_most_recent_dismissal_when_case_is_older_than_3yrs(self):
        case = CaseFactory.create()
        charge_1 = ChargeFactory.create_dismissed_charge(date=self.THREE_YEARS_AGO)
        charge_2 = ChargeFactory.create_dismissed_charge(date=self.THREE_YEARS_AGO)
        case.charges = [charge_1, charge_2]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_dismissal is None

    def test_expunger_sets_mrd_when_mrd_is_in_middle_of_list(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=self.TWO_YEARS_AGO)
        charge = ChargeFactory.create_dismissed_charge(date=self.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [charge, charge, mrd_charge, charge, charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_dismissal is mrd_charge

    def test_expunger_sets_mrd_when_mrd_is_at_end_of_list(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=self.TWO_YEARS_AGO)
        charge = ChargeFactory.create_dismissed_charge(date=self.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [charge, charge, mrd_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_dismissal is mrd_charge

    def test_it_sets_most_recent_conviction_from_the_last_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        case.charges = [mrc_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_conviction is mrc_charge

    def test_it_sets_the_second_most_recent_conviction_within_the_last_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(self.TWO_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Convicted')

        case.charges = [second_mrc_charge, mrc_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._second_most_recent_conviction is second_mrc_charge

    def test_it_does_not_set_mrc_when_greater_than_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(self.TEN_YEARS, 'Convicted')
        case.charges = [mrc_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_conviction is None

    def test_it_does_not_set_2nd_mrc_when_greater_than_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(self.TEN_YEARS, 'Convicted')
        case.charges = [mrc_charge, second_mrc_charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._second_most_recent_conviction is None

    def test_mrc_and_second_mrc(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(self.TWO_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        charge = ChargeFactory.create()
        charge.disposition = Disposition(self.TEN_YEARS, 'Convicted')
        case.charges = [charge, charge, second_mrc_charge, mrc_charge, charge, charge]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._most_recent_conviction is mrc_charge
        assert expunger._second_most_recent_conviction is second_mrc_charge

    def test_num_acquittals(self):
        case = CaseFactory.create()
        one_year_ago_dismissal = ChargeFactory.create_dismissed_charge(date=self.ONE_YEAR_AGO)
        two_year_ago_dismissal = ChargeFactory.create_dismissed_charge(date=self.TWO_YEARS_AGO)
        less_than_3_year_ago_dismissal = ChargeFactory.create_dismissed_charge(date=self.LESS_THAN_THREE_YEARS_AGO)
        three_year_ago_dismissal = ChargeFactory.create_dismissed_charge(date=self.THREE_YEARS_AGO)

        case.charges = [one_year_ago_dismissal, two_year_ago_dismissal, three_year_ago_dismissal, less_than_3_year_ago_dismissal]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._num_acquittals == 3

    def test_num_acquittals(self):
        case = CaseFactory.create()
        three_year_ago_dismissal = ChargeFactory.create_dismissed_charge(date=self.THREE_YEARS_AGO)

        case.charges = [three_year_ago_dismissal]

        expunger = Expunger([case])
        expunger.run()

        assert expunger._num_acquittals == 0
