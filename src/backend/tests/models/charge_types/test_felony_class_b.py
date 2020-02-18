import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest


class TestSingleChargeConvictionsFelonyClassB(ChargeTypeTest):
    def test_class_b_felony_164057(self):
        self.charge_dict["name"] = "Aggravated theft in the first degree"
        self.charge_dict["statute"] = "164.057"
        self.charge_dict["level"] = "Felony Class B"
        self.charge_dict["disposition"] = self.convicted
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, FelonyClassB)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_class_felony_is_added_to_b_felony_attribute(self):
        self.charge_dict["name"] = "Aggravated theft in the first degree"
        self.charge_dict["statute"] = "164.057"
        self.charge_dict["level"] = "Felony Class B"
        charge = self.create_recent_charge()

        assert isinstance(charge, FelonyClassB)
