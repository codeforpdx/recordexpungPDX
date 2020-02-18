import unittest

from datetime import datetime

from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest


class TestSingleChargeConvictionsFelonyClassC(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict = ChargeFactory.default_dict(disposition=self.convicted)
        self.charges = []

    # TODO: what is this test name?
    def test_misdemeanor_164055(self):
        self.charge_dict["name"] = "Theft in the first degree"
        self.charge_dict["statute"] = "164.055"
        self.charge_dict["level"] = "Felony Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, FelonyClassC)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
