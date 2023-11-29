from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.possible_traffic_violation import PossibleTrafficViolation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_violation_multnomah_convicted():
    charge = ChargeFactory.create(
        name="Viol Treatment",
        statute="1615662",
        level="Violation Unclassified",
        disposition=Dispositions.CONVICTED,
        location="Multnomah",
    )

    assert isinstance(charge.charge_type, PossibleTrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.type_eligibility.reason == "Either ineligible under 137.225(7)(a) or eligible under 137.225(5)(c)"


def test_violation_multnomah_dismissed():
    charge = ChargeFactory.create(
        name="Misdemeanor Treated as a Violation",
        statute="161.566(1)",
        level="Violation Class A",
        disposition=Dispositions.DISMISSED,
        location="Multnomah",
    )

    assert isinstance(charge.charge_type, PossibleTrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        charge.type_eligibility.reason
        == "Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge."
    )


def test_violation_multnomah_unrecognized_disposition():
    charge = ChargeFactory.create(
        name="(Reduced - DA Elected)",
        statute="164045",
        level="Violation Class A",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        location="Multnomah",
    )

    assert isinstance(charge.charge_type, PossibleTrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        charge.type_eligibility.reason
        == "A possibly-traffic-related violation with indeterminate disposition needs more information to determine eligibility."
    )
