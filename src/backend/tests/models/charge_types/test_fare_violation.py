from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.fare_violation import FareViolation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_fare_violation_convicted():
    charge = ChargeFactory.create(
        name="Fare Violation", statute="29.15", level="Violation Unclassified", disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charge.charge_type, FareViolation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_fare_violation_dismissed():
    charge = ChargeFactory.create(
        name="Fare Violation", statute="2915", level="Violation Unclassified", disposition=Dispositions.DISMISSED,
    )

    assert isinstance(charge.charge_type, FareViolation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(1)(b)"
