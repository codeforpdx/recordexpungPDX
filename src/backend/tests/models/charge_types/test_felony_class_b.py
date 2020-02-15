import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


class TestSingleChargeConvictionsFelonyClassB(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_class_b_felony_164057(self):
        self.single_charge["name"] = "Aggravated theft in the first degree"
        self.single_charge["statute"] = "164.057"
        self.single_charge["level"] = "Felony Class B"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, FelonyClassB)
        assert charge.type_name == "Felony Class B"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_class_felony_is_added_to_b_felony_attribute(self):
        self.single_charge["name"] = "Aggravated theft in the first degree"
        self.single_charge["statute"] = "164.057"
        self.single_charge["level"] = "Felony Class B"
        charge = self.create_recent_charge()

        assert isinstance(charge, FelonyClassB)
        assert charge.__class__.__name__ == "FelonyClassB"
