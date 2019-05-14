import unittest

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.models.disposition import Disposition
from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory


class TestChargeClass(unittest.TestCase):

    TEN_YEARS_AGO = (date.today() + relativedelta(years=-10)).strftime('%m/%d/%Y')
    LESS_THAN_TEN_YEARS_AGO = (date.today() + relativedelta(years=-10, days=+1)).strftime('%m/%d/%Y')
    LESS_THAN_THREE_YEARS_AGO = (date.today() + relativedelta(years=-3, days=+1)).strftime('%m/%d/%Y')
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3)).strftime('%m/%d/%Y')

    def setUp(self):
        self.charge = ChargeFactory.build()

    def test_it_initializes_simple_statute(self):
        self.charge['statute'] = '1231235B'
        charge = ChargeFactory.save(self.charge)

        assert charge.statute == '1231235B'

    def test_it_normalizes_statute(self):
        self.charge['statute'] = '-123.123(5)()B'
        charge = ChargeFactory.save(self.charge)

        assert charge.statute == '1231235B'

    def test_it_converts_statute_to_uppercase(self):
        self.charge['statute'] = '-123.123(5)()b'
        charge = ChargeFactory.save(self.charge)

        assert charge.statute == '1231235B'

    def test_it_retrieves_its_parent_instance(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(case=case)

        assert charge.case()() is case

    def test_it_knows_if_it_has_a_recent_conviction_happy_path(self):
        charge = ChargeFactory.create()
        charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Convicted')

        assert charge.recent_conviction() is True

    def test_it_knows_if_it_has_a_recent_conviction_sad_path(self):
        charge = ChargeFactory.create()
        charge.disposition = Disposition(self.TEN_YEARS_AGO, 'Convicted')

        assert charge.recent_conviction() is False

    def test_dismissed_charge_is_not_a_recent_conviction(self):
        charge = ChargeFactory.create()
        charge.disposition = Disposition(self.LESS_THAN_TEN_YEARS_AGO, 'Dismissed')

        assert charge.recent_conviction() is False

    def test_most_recent_acquittal_happy_path(self):
        charge = ChargeFactory.create(date=self.LESS_THAN_THREE_YEARS_AGO)
        charge.disposition = Disposition(ruling='Dismissed')

        assert charge.recent_acquittal() is True

    def test_most_recent_acquittal_sad_path(self):
        charge = ChargeFactory.create(date=self.THREE_YEARS_AGO)
        charge.disposition = Disposition(ruling='Dismissed')

        assert charge.recent_acquittal() is False

    def test_convicted_charge_is_not_a_recent_acquittal(self):
        charge = ChargeFactory.create(date=self.LESS_THAN_THREE_YEARS_AGO)
        charge.disposition = Disposition(ruling='Convicted')

        assert charge.recent_acquittal() is False
