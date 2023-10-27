from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.violation import Violation
from expungeservice.record_merger import RecordMerger
from expungeservice.models.charge_types.traffic_violation import TrafficViolation

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
    
def test_violation_multnomah_convicted():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.CONVICTED, location="Multnomah"
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Traffic Violation – Ineligible under 137.225(7)(a) OR Violation – Eligible under 137.225(5)(c)"
    )
    assert isinstance(charges[0].charge_type, TrafficViolation)
    assert isinstance(charges[1].charge_type, Violation)


def test_violation_multnomah_dismissed():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Viol Treatment", statute="1615662", level="Violation Unclassified", disposition=Dispositions.DISMISSED, location="Multnomah"
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Traffic Violation – Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge. OR Violation – Eligible under 137.225(1)(b)"
    )
    assert isinstance(charges[0].charge_type, TrafficViolation)
    assert isinstance(charges[1].charge_type, Violation)
