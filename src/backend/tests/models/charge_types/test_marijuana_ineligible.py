from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_marijuana_ineligible_statute_475b3493c():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Unlawful Manufacture of Marijuana Item"
    charge_dict["statute"] = "475B.349(3)(C)"
    charge_dict["level"] = "Felony Class C"
    marijuana_felony_class_c = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_felony_class_c, MarijuanaIneligible)
    assert marijuana_felony_class_c.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_c.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_c.expungement_result.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b359():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
    charge_dict["statute"] = "475b.359"
    charge_dict["level"] = "Felony Class A"
    marijuana_felony_class_a = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b367():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Causing another person to ingest marijuana"
    charge_dict["statute"] = "475B.367"
    charge_dict["level"] = "Felony Class A"
    marijuana_felony_class_a = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b371():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Administration to another person under 18 years of age"
    charge_dict["statute"] = "475B.371"
    charge_dict["level"] = "Felony Class A"
    marijuana_felony_class_a = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_167262():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Use of minor in controlled substance or marijuana item offense"
    charge_dict["statute"] = "167.262"
    charge_dict["level"] = "Misdemeanor Class A"
    marijuana_misdemeanor_class_a = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_misdemeanor_class_a, MarijuanaIneligible)
    assert marijuana_misdemeanor_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b3592a():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
    charge_dict["statute"] = "475b.359(2)(a)"
    charge_dict["level"] = "Felony Class A"
    marijuana_felony_class_a = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"
