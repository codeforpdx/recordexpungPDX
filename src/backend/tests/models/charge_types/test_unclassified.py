import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeUnclassified(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(ruling="Dismissed", date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_unclassified_charge(self):
        self.single_charge["name"] = "Assault in the ninth degree"
        self.single_charge["statute"] = "333.333"
        self.single_charge["level"] = "Felony Class F"
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


class TestSingleChargeConvictionsUnclassified(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    # Eligible misdemeanor and class C felony tests

    def test_charge_that_falls_through(self):
        self.single_charge["name"] = "Aggravated theft in the first degree"
        self.single_charge["statute"] = "164.057"
        self.single_charge["level"] = "Felony Class F"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, UnclassifiedCharge)
        assert charge.type_name == "Unclassified"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"
