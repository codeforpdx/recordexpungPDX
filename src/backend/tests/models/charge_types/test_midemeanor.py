from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_misdemeanor_missing_disposition():
    misdemeanor_charge = ChargeFactory.create(
        name="Criminal Trespass in the Second Degree", statute="164.245", level="Misdemeanor Class C", disposition=None
    )

    assert isinstance(misdemeanor_charge, Misdemeanor)
    assert misdemeanor_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        misdemeanor_charge.type_eligibility.reason
        == "Misdemeanors are always eligible under 137.225(5)(b) for convictions, or 137.225(1)(b) for dismissals"
    )


def test_misdemeanor_164043():
    charge = ChargeFactory.create(
        name="Theft in the third degree",
        statute="164.043",
        level="Misdemeanor Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charge, Misdemeanor)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_misdemeanor_164125():
    charge = ChargeFactory.create(
        name="Theft of services", statute="164.125", level="Misdemeanor Class A", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, Misdemeanor)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_drug_free_zone_variance_misdemeanor():
    charge = ChargeFactory.create(
        name="	Drug Free Zone Variance",
        statute="14B20060",
        level="Misdemeanor Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charge, Misdemeanor)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(b)"
