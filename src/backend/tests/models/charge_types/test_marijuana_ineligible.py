from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_marijuana_ineligible_statute_475b3493c():
    marijuana_felony_class_c = ChargeFactory.create(
        name="Unlawful Manufacture of Marijuana Item",
        statute="475B.349(3)(C)",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_felony_class_c, MarijuanaIneligible)
    assert marijuana_felony_class_c.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_c.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_c.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b359():
    marijuana_felony_class_a = ChargeFactory.create(
        name="Arson incident to manufacture of cannabinoid extract in first degree",
        statute="475b.359",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b367():
    marijuana_felony_class_a = ChargeFactory.create(
        name="Causing another person to ingest marijuana",
        statute="475B.367",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b371():
    marijuana_felony_class_a = ChargeFactory.create(
        name="Administration to another person under 18 years of age",
        statute="475B.371",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_167262():
    marijuana_misdemeanor_class_a = ChargeFactory.create(
        name="Use of minor in controlled substance or marijuana item offense",
        statute="167.262",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_misdemeanor_class_a, MarijuanaIneligible)
    assert marijuana_misdemeanor_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_misdemeanor_class_a.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_misdemeanor_class_a.type_eligibility.reason == "Ineligible under 137.226"


def test_marijuana_ineligible_statute_475b3592a():
    marijuana_felony_class_a = ChargeFactory.create(
        name="Arson incident to manufacture of cannabinoid extract in first degree",
        statute="475b.359(2)(a)",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_felony_class_a, MarijuanaIneligible)
    assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
    assert marijuana_felony_class_a.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert marijuana_felony_class_a.type_eligibility.reason == "Ineligible under 137.226"
