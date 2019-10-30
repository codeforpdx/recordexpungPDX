import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeAcquittals(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.single_charge['disposition'] = Disposition(ruling='Acquitted', date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_acquitted = self.create_recent_charge()
        self.charges.append(felony_class_a_acquitted)

        assert felony_class_a_acquitted.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_acquitted.expungement_result.type_eligibility.reason == 'Eligible under 137.225(1)(b)'


class TestSingleChargeDismissals(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.single_charge['disposition'] = Disposition(ruling='Dismissed', date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)

        assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_dismissed.expungement_result.type_eligibility.reason == 'Eligible under 137.225(1)(b)'


class TestSingleChargeNoComplaint(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.single_charge['disposition'] = Disposition(date=last_week, ruling='No Complaint')
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_no_complaint = self.create_recent_charge()
        self.charges.append(felony_class_a_no_complaint)

        assert felony_class_a_no_complaint.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_no_complaint.expungement_result.type_eligibility.reason == 'Eligible under 137.225(1)(b)'
