from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaViolation
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_marijuana_violation_conviction():
    marijuana_violation = ChargeFactory.create(
        name="Possession of Marijuana < 1 Ounce",
        statute="4758643",
        level="Violation Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_violation.charge_type, MarijuanaViolation)
    assert marijuana_violation.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert marijuana_violation.type_eligibility.reason == "Eligible under 475B.401"


def test_marijuana_violation_dismissal():
    marijuana_violation = ChargeFactory.create(
        name="Unlawful Possession of less than One Ounce of Marijuana",
        statute="4758643C",
        level="Violation Unclassified",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(marijuana_violation.charge_type, MarijuanaViolation)
    assert marijuana_violation.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert marijuana_violation.type_eligibility.reason == "Dismissed violations are eligible under 137.225(1)(b)"
