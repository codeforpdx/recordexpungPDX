import unittest

from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.record_factory import RecordFactory

class TestRecordObject(unittest.TestCase):

    def test_print_balance_in_cents(self):

        recordTest = RecordFactory.create([CaseFactory.create(balance = '123.00'),
                                           CaseFactory.create(balance = '246.00')])

        assert recordTest.total_balance_due == 369.00

    def test_print_balance_in_cents_empty(self):

        recordTest = RecordFactory.create([CaseFactory.create()])

        assert recordTest.total_balance_due == 0.00

class TestChargeMethod(unittest.TestCase):
    def setUp(self):
        self.case_zero = CaseFactory.create()
        self.charge_zero = ChargeFactory.create(case=self.case_zero)
        self.case_zero.charges = [self.charge_zero]
        
        self.case_one = CaseFactory.create()
        self.charge_one = ChargeFactory.create(case=self.case_one)
        self.charge_two = ChargeFactory.create(case=self.case_one)
        self.case_one.charges = [self.charge_one, self.charge_two]
        
        self.record = RecordFactory.create([self.case_zero, self.case_one])

    def test_num_cases(self):
        assert len(self.record.charges) == 3
        
    def test_charges_index_0(self):
        assert self.record.charges[0] == self.charge_zero

    def test_charges_index_1(self):
        assert self.record.charges[1] == self.charge_one

    def test_charges_index_2(self):
        assert self.record.charges[2] == self.charge_two

