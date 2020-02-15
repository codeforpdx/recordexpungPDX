import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictionsMarijuanaIneligible(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_marijuana_ineligible_statute_475b3493c(self):
        self.single_charge["name"] = "Unlawful Manufacture of Marijuana Item"
        self.single_charge["statute"] = "475B.349(3)(C)"
        self.single_charge["level"] = "Felony Class C"
        marijuana_felony_class_c = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_c)

        assert isinstance(marijuana_felony_class_c, MarijuanaIneligible)
        assert marijuana_felony_class_c.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_c.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_c.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b359(self):
        self.single_charge["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.single_charge["statute"] = "475b.359"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b367(self):
        self.single_charge["name"] = "Causing another person to ingest marijuana"
        self.single_charge["statute"] = "475B.367"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b371(self):
        self.single_charge["name"] = "Administration to another person under 18 years of age"
        self.single_charge["statute"] = "475B.371"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_167262(self):
        self.single_charge["name"] = "Use of minor in controlled substance or marijuana item offense"
        self.single_charge["statute"] = "167.262"
        self.single_charge["level"] = "Misdemeanor Class A"
        marijuana_misdemeanor_class_a = self.create_recent_charge()
        self.charges.append(marijuana_misdemeanor_class_a)

        assert isinstance(marijuana_misdemeanor_class_a, MarijuanaIneligible)
        assert marijuana_misdemeanor_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b3592a(self):
        self.single_charge["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.single_charge["statute"] = "475b.359(2)(a)"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"
