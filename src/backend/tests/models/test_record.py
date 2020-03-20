import unittest

from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestRecordObject(unittest.TestCase):
    def test_print_balance_in_cents(self):

        recordTest = Record([CaseFactory.create(balance="123.00"), CaseFactory.create(balance="246.00")])

        assert recordTest.total_balance_due == 369.00

    def test_print_balance_in_cents_empty(self):

        recordTest = Record([CaseFactory.create()])

        assert recordTest.total_balance_due == 0.00


class TestChargeMethod(unittest.TestCase):
    def setUp(self):
        self.case_1 = CaseFactory.create(case_number="1")
        self.charge_zero = ChargeFactory.create(case_number=self.case_1.case_number)
        self.case_1.charges = [self.charge_zero]

        self.case_2 = CaseFactory.create(case_number="2")
        self.charge_one = ChargeFactory.create(case_number=self.case_2.case_number)
        self.charge_two = ChargeFactory.create(case_number=self.case_2.case_number)
        self.case_2.charges = [self.charge_one, self.charge_two]

        self.record = Record([self.case_1, self.case_2])

    def test_num_cases(self):
        assert len(self.record.charges) == 3

    def test_charges_index_0(self):
        assert self.record.charges[0] == self.charge_zero

    def test_charges_index_1(self):
        assert self.record.charges[1] == self.charge_one

    def test_charges_index_2(self):
        assert self.record.charges[2] == self.charge_two
