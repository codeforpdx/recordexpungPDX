from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.violation import Violation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_violation_convicted():
    charge = ChargeFactory.create(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, Violation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(d)"


def test_violation_dismissed():
    charge = ChargeFactory.create(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge, Violation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Dismissed violations are ineligible by omission from statute"
