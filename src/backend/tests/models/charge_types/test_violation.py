from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.violation import Violation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_violation():
    charge = ChargeFactory.create(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, Violation)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(d)"
