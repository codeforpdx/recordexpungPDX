import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


class TestSingleChargeConvictionsFelonyClassC(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_misdemeanor_164055(self):
        self.single_charge["name"] = "Theft in the first degree"
        self.single_charge["statute"] = "164.055"
        self.single_charge["level"] = "Felony Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, FelonyClassC)
        assert charge.type_name == "Felony Class C"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
