import unittest

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory


class TestCaseWithDisposition(unittest.TestCase):

    def setUp(self):
        self.charge = {'name': 'PCS', 'level': 'Misdemeanor', 'date': '12/12/1999'}

    def test_it_initializes_simple_statute(self):
        self.charge['statute'] = '1231235B'
        charge = ChargeFactory.create(**self.charge)

        assert charge.statute == '1231235B'

    def test_it_normalizes_statute(self):
        self.charge['statute'] = '-123.123(5)()B'
        charge = ChargeFactory.create(**self.charge)

        assert charge.statute == '1231235B'

    def test_it_converts_statute_to_uppercase(self):
        self.charge['statute'] = '-123.123(5)()b'
        charge = ChargeFactory.create(**self.charge)

        assert charge.statute == '1231235B'
