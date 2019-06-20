import unittest

from expungeservice.models.case import Case
from expungeservice.models.record_object import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory

class TestRecordObject(unittest.TestCase):

    def setUp(self):
        self.list_cases = []
        self.list_charges = []

        self.charge1 = ChargeFactory.build()

        self.list_charges.append(self.charge1)

        self.case1 = Case(("John Doe", "1990"), "", "", ("1/1/2019",""), ("",""), self.list_charges, "")
        self.case2 = Case(("John Doe", "1991"), "", "", ("1/2/2019",""), ("",""), self.list_charges, "")

        self.case1.set_balance_due("123")
        self.case2.set_balance_due("246")

        self.list_cases.append(self.case1)
        self.list_cases.append(self.case2)

        self.record = Record(self.list_cases)

    def test_print_balance_in_cents(self):
        assert self.record.total_balance_due() == 369.0

    def test_print_list_charges(self):
        assert self.record.charges()[0] == self.list_charges[0]
        assert self.record.charges()[1] == self.list_charges[0]
