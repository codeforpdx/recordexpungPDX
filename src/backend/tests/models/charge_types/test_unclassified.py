import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.disposition import Disposition

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest


class TestSingleChargeUnclassified(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict = ChargeFactory.default_dict(disposition=self.dismissed)
        self.charges = []

    def test_unclassified_charge(self):
        self.charge_dict["name"] = "Assault in the ninth degree"
        self.charge_dict["statute"] = "333.333"
        self.charge_dict["level"] = "Felony Class F"
        unclassified_dismissed = self.create_recent_charge()
        self.charges.append(unclassified_dismissed)

        assert isinstance(unclassified_dismissed, UnclassifiedCharge)
        assert (
            unclassified_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        )
        assert (
            unclassified_dismissed.expungement_result.type_eligibility.reason
            == "Unrecognized Charge : Further Analysis Needed"
        )

    def test_charge_that_falls_through(self):
        self.charge_dict["name"] = "Aggravated theft in the first degree"
        self.charge_dict["statute"] = "164.057"
        self.charge_dict["level"] = "Felony Class F"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, UnclassifiedCharge)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"
