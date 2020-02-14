import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.disposition import Disposition

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTestsParent


class TestSingleChargeConvictionsMarijuanaIneligible(ChargeTypeTestsParent):
    def setUp(self):
        ChargeTypeTestsParent.setUp(self)
        last_week = datetime.today() - timedelta(days=7)
        self.charge_dict = ChargeFactory.default_dict(disposition=self.convicted)
        self.charges = []

    def test_marijuana_ineligible_statute_475b3493c(self):
        self.charge_dict["name"] = "Unlawful Manufacture of Marijuana Item"
        self.charge_dict["statute"] = "475B.349(3)(C)"
        self.charge_dict["level"] = "Felony Class C"
        marijuana_felony_class_c = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_c)

        assert isinstance(marijuana_felony_class_c, MarijuanaIneligible)
        assert marijuana_felony_class_c.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_c.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_c.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b359(self):
        self.charge_dict["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.charge_dict["statute"] = "475b.359"
        self.charge_dict["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b367(self):
        self.charge_dict["name"] = "Causing another person to ingest marijuana"
        self.charge_dict["statute"] = "475B.367"
        self.charge_dict["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b371(self):
        self.charge_dict["name"] = "Administration to another person under 18 years of age"
        self.charge_dict["statute"] = "475B.371"
        self.charge_dict["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_167262(self):
        self.charge_dict["name"] = "Use of minor in controlled substance or marijuana item offense"
        self.charge_dict["statute"] = "167.262"
        self.charge_dict["level"] = "Misdemeanor Class A"
        marijuana_misdemeanor_class_a = self.create_recent_charge()
        self.charges.append(marijuana_misdemeanor_class_a)

        assert isinstance(marijuana_misdemeanor_class_a, MarijuanaIneligible)
        assert marijuana_misdemeanor_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b3592a(self):
        self.charge_dict["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.charge_dict["statute"] = "475b.359(2)(a)"
        self.charge_dict["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"
