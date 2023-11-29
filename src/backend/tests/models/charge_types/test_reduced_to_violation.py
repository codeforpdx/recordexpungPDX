from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_reduced_to_violation_convicted():
    charge = ChargeFactory.create(
        name="Theft in the Second Degree (Reduced - DA Elected)",
        statute="164045",
        level="Violation Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charge.charge_type, ReducedToViolation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(d)"


def test_reduced_to_violation_dismissed():
    charge = ChargeFactory.create(
        name="Misdemeanor Treated as a Violation",
        statute="161.566(1)",
        level="Violation Class A",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(charge.charge_type, ReducedToViolation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissed criminal charge eligible under 137.225(1)(b)"


def test_reduced_violation_ineligible_under_other_criterion():
    charge = ChargeFactory.create(
        name="Criminal Driving While Suspended\n (Reduced - DA Elected)", statute="8111824", level="Violation Class A",
    )

    assert not isinstance(charge.charge_type, ReducedToViolation)
