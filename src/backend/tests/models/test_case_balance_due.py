import unittest

from expungeservice.models.case import Case


class TestCaseBalanceDue(unittest.TestCase):

    def setUp(self):
        self.case = Case(("John Doe", "1990"), "", "", ("1/1/2019",""), ("",""), "", "")

    def test_balance_due_getter_setter(self):     

        self.case.set_balance_due("123.45")
        assert self.case.get_balance_due() == 123.45

        self.case.set_balance_due("2,345.67")
        assert self.case.get_balance_due() == 2345.67
        
        self.case.set_balance_due(12345.67)
        assert self.case.get_balance_due() == 12345.67

        self.case.set_balance_due("0")
        assert self.case.get_balance_due() == 0  
