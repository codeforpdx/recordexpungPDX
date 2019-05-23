import unittest

from datetime import datetime, timedelta
from expungeservice.expunger.analyzers.type_analyzer import TypeAnalyzer
from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.charge import Disposition


class TestSingleChargeAcquittals(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.acquitted_disposition = {'ruling': 'Acquitted', 'date': last_week}
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        charge.disposition = Disposition(**self.acquitted_disposition)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_acquitted = self.create_recent_charge()
        self.charges.append(felony_class_a_acquitted)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a_acquitted.expungement_result.type_eligibility is True
        assert felony_class_a_acquitted.expungement_result.type_eligibility_reason == 'Eligible under 137.225(1)(b)'

class TestSingleChargeDismissals(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.dismissed_disposition = {'ruling': 'Dismissed', 'date': last_week}
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        charge.disposition = Disposition(**self.dismissed_disposition)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a_dismissed.expungement_result.type_eligibility is True
        assert felony_class_a_dismissed.expungement_result.type_eligibility_reason == 'Eligible under 137.225(1)(b)'

class TestSingleChargeNoComplaint(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.acquitted_disposition = {'ruling': 'No Complaint', 'date': last_week}
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        charge.disposition = Disposition(**self.acquitted_disposition)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_no_complaint = self.create_recent_charge()
        self.charges.append(felony_class_a_no_complaint)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a_no_complaint.expungement_result.type_eligibility is True
        assert felony_class_a_no_complaint.expungement_result.type_eligibility_reason == 'Eligible under 137.225(1)(b)'
