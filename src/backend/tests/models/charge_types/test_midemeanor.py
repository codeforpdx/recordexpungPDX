import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.misdemeanor import Misdemeanor

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictionsMisdemeanor(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_misdemeanor(self):
        self.single_charge["name"] = "Criminal Trespass in the Second Degree"
        self.single_charge["statute"] = "164.245"
        self.single_charge["level"] = "Misdemeanor Class C"
        misdemeanor_charge = self.create_recent_charge()
        self.charges.append(misdemeanor_charge)

        assert isinstance(misdemeanor_charge, Misdemeanor)
        assert misdemeanor_charge.type_name == "Misdemeanor"
        assert misdemeanor_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert misdemeanor_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_misdemeanor_164043(self):
        self.single_charge["name"] = "Theft in the third degree"
        self.single_charge["statute"] = "164.043"
        self.single_charge["level"] = "Misdemeanor Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_misdemeanor_164125(self):
        self.single_charge["name"] = "Theft of services"
        self.single_charge["statute"] = "164.125"
        self.single_charge["level"] = "Misdemeanor Class A"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_drug_free_zone_variance_misdemeanor(self):
        self.single_charge["name"] = "	Drug Free Zone Variance"
        self.single_charge["statute"] = "14B20060"
        self.single_charge["level"] = "Misdemeanor Unclassified"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
