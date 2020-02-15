import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictionsNonTrafficViolation(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_non_traffic_violation(self):
        self.single_charge["name"] = "Viol Treatment"
        self.single_charge["statute"] = "1615662"
        self.single_charge["level"] = "Violation Unclassified"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, NonTrafficViolation)
        assert charge.type_name == "Non-traffic Violation"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(d)"
