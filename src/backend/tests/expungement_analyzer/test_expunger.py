import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expungement_analyzer.expunger import Expunger
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestExpungementAnalyzerUnitTests(unittest.TestCase):

    LESS_THAN_THREE_YEARS_AGO = (date.today() + relativedelta(years=-3, days=+1)).strftime('%m/%d/%Y')
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3)).strftime('%m/%d/%Y')
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2)).strftime('%m/%d/%Y')

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
