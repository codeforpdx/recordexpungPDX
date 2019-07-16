import unittest

from expungeservice.models.case import Case
from expungeservice.models.record_object import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.record_factory import RecordFactory

class TestRecordObject(unittest.TestCase):

    def test_print_balance_in_cents(self):

        recordTest = RecordFactory.create([CaseFactory.create(balance = '123.00'),
                                           CaseFactory.create(balance = '246.00')])

        assert recordTest.total_balance_due() == 369.00

    def test_print_balance_in_cents_empty(self):

        recordTest = RecordFactory.create([CaseFactory.create()])

        assert recordTest.total_balance_due() == 0.00

    def test_print_list_charges(self):
        
        recordTest = RecordFactory.create([CaseFactory.create(charges = [ChargeFactory.build()])]) 

        assert recordTest.charges()[0]['name'] == ChargeFactory.build()['name']



















