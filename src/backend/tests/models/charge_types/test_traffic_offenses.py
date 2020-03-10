"""
Rules for 800 Level charges are as follows:

800 level misdemeanors and felonies are eligible Only If the case was dismissed
800 level cases of any kind that are convicted are not eligible
800 level infractions do not block other cases
800 level misdemeanor and felony convictions do block
800 level misdemeanor and felony arrests block like other arrests
800 level convictions of any kind are not type eligible
"""

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.duii import Duii

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


# TODO: we can separate these three types to different test files too.
def test_traffic_violation_min_statute():
    charge = ChargeFactory.create(statute="801.000", level="Violation")

    assert isinstance(charge, TrafficViolation)


def test_traffic_violation_max_statute():
    charge = ChargeFactory.create(statute="825.999", level="Violation")

    assert isinstance(charge, TrafficViolation)


def test_convicted_violation_is_not_type_eligible():
    charge = ChargeFactory.create(
        statute="801.000", level="Class C Traffic Violation", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert not charge.blocks_other_charges()


def test_dismissed_violation_is_not_type_eligible():
    charge = ChargeFactory.create(
        statute="801.000", level="Class C Traffic Violation", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Dismissed violations are ineligible by omission from statute"
    assert not charge.blocks_other_charges()


def test_convicted_infraction_is_not_type_eligible():
    charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=Dispositions.CONVICTED)

    assert isinstance(charge, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert not charge.blocks_other_charges()


def test_dismissed_infraction_is_not_type_eligible():
    charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=Dispositions.DISMISSED)

    assert isinstance(charge, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Dismissed violations are ineligible by omission from statute"
    assert not charge.blocks_other_charges()


def test_no_dispo_violation_is_not_type_eligible():
    charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=None)

    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
    assert not charge.blocks_other_charges()


def test_unrecognized_violation_is_not_type_eligible():
    charge = ChargeFactory.create(
        statute="801.000", level="Class C Traffic Violation", disposition=Dispositions.UNRECOGNIZED_DISPOSITION
    )

    assert isinstance(charge, TrafficViolation)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
    assert not charge.blocks_other_charges()


"""
800 level misdemeanors and felonies are eligible Only If the case was dismissed
"""


def test_misdemeanor_conviction_is_not_eligible():
    charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=Dispositions.CONVICTED)

    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert charge.blocks_other_charges()


def test_misdemeanor_dismissal_is_eligible():
    charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=Dispositions.DISMISSED)

    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    assert charge.blocks_other_charges()


def test_felony_conviction_is_not_eligible():
    charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=Dispositions.CONVICTED)

    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
    assert charge.blocks_other_charges()


def test_felony_dismissal_is_eligible():
    charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=Dispositions.DISMISSED)

    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    assert charge.blocks_other_charges()


def test_duii():
    charge = ChargeFactory.create(statute="813.010")

    assert isinstance(charge, Duii)
