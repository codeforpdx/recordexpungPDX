import unittest

from datetime import datetime, timedelta
from expungeservice.expungement_analyzer.type_analyzer import TypeAnalyzer
from expungeservice.crawler.models.charge import Charge
from expungeservice.crawler.models.charge import Disposition


class TestSingleChargeConvictions(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        one_month_ago = (datetime.today() - timedelta(days=30)).strftime('%m/%d/%Y')
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = {'name': '', 'statute': '', 'level': '', 'date': one_month_ago}
        disposition = {'ruling': 'Convicted', 'date': last_week}
        self.convicted_disposition = Disposition(**disposition)
        self.charges = []

    def create_recent_charge(self):
        charge = Charge(**self.single_charge)
        charge.disposition = self.convicted_disposition
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a = self.create_recent_charge()
        self.charges.append(felony_class_a)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a.expungement_result.type_eligibility is False
        assert felony_class_a.expungement_result.reason == 'Ineligible under 137.225(5)'


class TestSingleChargeDismissals(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        one_month_ago = (datetime.today() - timedelta(days=30)).strftime('%m/%d/%Y')
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = {'name': '', 'statute': '', 'level': '', 'date': one_month_ago}
        disposition = {'ruling': 'Dismissed', 'date': last_week}
        self.dismissed_disposition = Disposition(**disposition)
        self.charges = []

    def create_recent_charge(self):
        charge = Charge(**self.single_charge)
        charge.disposition = self.dismissed_disposition
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a = self.create_recent_charge()
        self.charges.append(felony_class_a)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a.expungement_result.type_eligibility is True
        assert felony_class_a.expungement_result.reason == 'Eligible under 137.225(1)(b)'


class TestSingleChargeAcquittals(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        one_month_ago = (datetime.today() - timedelta(days=30)).strftime('%m/%d/%Y')
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = {'name': '', 'statute': '', 'level': '', 'date': one_month_ago}
        disposition = {'ruling': 'Acquitted', 'date': last_week}
        self.acquitted_disposition = Disposition(**disposition)
        self.charges = []

    def create_recent_charge(self):
        charge = Charge(**self.single_charge)
        charge.disposition = self.acquitted_disposition
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_acquitted = self.create_recent_charge()
        self.charges.append(felony_class_a_acquitted)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a_acquitted.expungement_result.type_eligibility is True
        assert felony_class_a_acquitted.expungement_result.reason == 'Eligible under 137.225(1)(b)'
