from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.record_merger import RecordMerger

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_reduced_to_violation_convicted():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Theft in the Second Degree (Reduced - DA Elected)",
        statute="164045",
        level="Violation Class A",
        disposition=Dispositions.CONVICTED,
    )[1]

    assert isinstance(charge.charge_type, ReducedToViolation)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(5)(d)"


def test_reduced_to_violation_dismissed():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Misdemeanor Treated as a Violation",
        statute="161.566(1)",
        level="Violation Class A",
        disposition=Dispositions.DISMISSED,
    )

    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Traffic Violation – Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge. OR Reduced to Violation – Dismissed criminal charge eligible under 137.225(1)(b)"
    )
    assert isinstance(charges[0].charge_type, TrafficViolation)
    assert isinstance(charges[1].charge_type, ReducedToViolation)


def test_reduced_to_violation_unrecognized_disposition():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Theft in the Second Degree (Reduced - DA Elected)",
        statute="164045",
        level="Violation Class A",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Traffic Violation – Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals) OR Reduced to Violation – Reduced Violations are always eligible under 137.225(5)(d) for convictions, or 137.225(1)(b) for dismissals"
    )
    assert isinstance(charges[0].charge_type, TrafficViolation)
    assert isinstance(charges[1].charge_type, ReducedToViolation)


def test_reduced_violation_ineligible_under_other_criterion():
    charge = ChargeFactory.create(
        name="Criminal Driving While Suspended\n (Reduced - DA Elected)", statute="8111824", level="Violation Class A",
    )

    assert not isinstance(charge.charge_type, ReducedToViolation)
