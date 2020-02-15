import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


class TestSingleChargeConvictionsFelonyClassA(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_convicted = self.create_recent_charge()
        self.charges.append(felony_class_a_convicted)

        assert isinstance(felony_class_a_convicted, FelonyClassA)
        assert felony_class_a_convicted.type_name == "Felony Class A"
        assert felony_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert felony_class_a_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"


class TestSingleChargeAcquittalsFelonyClassA(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(ruling="Acquitted", date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)

        assert isinstance(felony_class_a_dismissed, FelonyClassA)
        assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_dismissed.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"


class TestSingleChargeDismissalsFelonyClassA(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(ruling="Dismissed", date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)

        assert isinstance(felony_class_a_dismissed, FelonyClassA)
        assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_dismissed.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"


class TestSingleChargeNoComplaint(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(date=last_week, ruling="No Complaint")
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_no_complaint = self.create_recent_charge()
        self.charges.append(felony_class_a_no_complaint)

        assert isinstance(felony_class_a_no_complaint, FelonyClassA)
        assert felony_class_a_no_complaint.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_no_complaint.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"
