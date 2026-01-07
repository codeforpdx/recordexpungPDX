"""
Rules for 800 Level charges are as follows:

800 level misdemeanors and felonies are eligible Only If the case was dismissed
800 level cases of any kind that are convicted are not eligible
800 level infractions do not block other cases
800 level misdemeanor and felony convictions do block
800 level misdemeanor and felony arrests block like other arrests
800 level convictions of any kind are not type eligible
"""
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.duii import DivertedDuii

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


# TODO: we can separate these three types to different test files too.
def test_traffic_violation_min_statute():
    charge = ChargeFactory.create(statute="801.000", level="Violation")

    assert isinstance(charge.charge_type, TrafficViolation)


def test_traffic_violation_max_statute():
    charge = ChargeFactory.create(statute="825.999", level="Violation")

    assert isinstance(charge.charge_type, TrafficViolation)


def test_convicted_violation_is_not_type_eligible():
    charge = ChargeFactory.create(
        statute="801.000", level="Class C Traffic Violation", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert not charge.charge_type.blocks_other_charges


def test_dismissed_violation_is_not_type_eligible():
    charge = ChargeFactory.create(
        statute="801.000", level="Class C Traffic Violation", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
    assert not charge.charge_type.blocks_other_charges


def test_convicted_infraction_is_not_type_eligible():
    charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=Dispositions.CONVICTED)

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert not charge.charge_type.blocks_other_charges


def test_dismissed_infraction_is_not_type_eligible():
    charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=Dispositions.DISMISSED)

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
    assert not charge.charge_type.blocks_other_charges


def test_traffic_infraction_without_statute():
    charge = ChargeFactory.create(level="Infraction Class B")
    assert isinstance(charge.charge_type, TrafficViolation)


def test_old_traffic_statute():
    charge = ChargeFactory.create(
        statute="483050", name="Defective Equipment", level="Infraction Class B", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
    assert not charge.charge_type.blocks_other_charges


"""
800 level misdemeanors and felonies are eligible Only If the case was dismissed
"""


def test_misdemeanor_conviction_is_not_eligible():
    charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=Dispositions.CONVICTED)

    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert charge.charge_type.blocks_other_charges


def test_misdemeanor_dismissal_is_eligible():
    charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=Dispositions.DISMISSED)

    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(d)"
    assert charge.charge_type.blocks_other_charges


def test_felony_conviction_is_not_eligible():
    charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=Dispositions.CONVICTED)

    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert charge.charge_type.blocks_other_charges


def test_felony_dismissal_is_eligible():
    charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=Dispositions.DISMISSED)

    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(d)"
    assert charge.charge_type.blocks_other_charges


def test_duii():
    charges = ChargeFactory.create_ambiguous_charge(statute="813.010", disposition=Dispositions.DISMISSED)

    assert isinstance(charges[0].charge_type, DivertedDuii)
    assert isinstance(charges[1].charge_type, DismissedCharge)


def test_pedestrian_jwalking():
    charge = ChargeFactory.create(name="Pedestrian J-Walking", statute="1634020", level="Infraction Unclassified")
    assert isinstance(charge.charge_type, TrafficViolation)
