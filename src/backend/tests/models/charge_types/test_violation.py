from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.violation import Violation
from expungeservice.record_merger import RecordMerger
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.possible_traffic_violation import PossibleTrafficViolation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_violation_convicted():
    charge = ChargeFactory.create(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge.charge_type, Violation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_violation_dismissed():
    charge = ChargeFactory.create(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge.charge_type, Violation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(1)(b)"
