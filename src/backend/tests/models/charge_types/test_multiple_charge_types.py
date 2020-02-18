import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.traffic_violation import TrafficViolation

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition
from tests.models.test_charge import ChargeTypeTest


class TestMultipleCharges(ChargeTypeTest):
    # def setUp(self):

    def test_two_charges(self):
        # first charge
        self.charge_dict["name"] = "Theft of services"
        self.charge_dict["statute"] = "164.125"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.convicted
        charge = self.create_recent_charge()
        self.charges.append(charge)

        # second charge
        self.charge_dict["name"] = "Traffic Violation"
        self.charge_dict["statute"] = "801.000"
        self.charge_dict["level"] = "Class C Traffic Violation"
        self.charge_dict["disposition"] = self.convicted
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(self.charges[0], Misdemeanor)
        assert self.charges[0].expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.charges[0].expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

        assert isinstance(self.charges[1], TrafficViolation)
        assert self.charges[1].expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert self.charges[1].expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"

    def test_multiple_class_b_felonies_are_added_to_b_felony_list(self):
        # first charge
        self.charge_dict["name"] = "Theft of services"
        self.charge_dict["statute"] = "164.125"
        self.charge_dict["level"] = "Misdemeanor Class A"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        # B felony
        self.charge_dict["name"] = "Aggravated theft in the first degree"
        self.charge_dict["statute"] = "164.057"
        self.charge_dict["level"] = "Felony Class B"
        charge_1 = self.create_recent_charge()
        self.charges.append(charge_1)

        # Second B felony
        self.charge_dict["name"] = "Aggravated theft in the first degree"
        self.charge_dict["statute"] = "164.057"
        self.charge_dict["level"] = "Felony Class B"
        charge_2 = self.create_recent_charge()
        self.charges.append(charge_2)

        assert isinstance(self.charges[0], Misdemeanor)
        assert isinstance(self.charges[1], FelonyClassB)
        assert isinstance(self.charges[2], FelonyClassB)
