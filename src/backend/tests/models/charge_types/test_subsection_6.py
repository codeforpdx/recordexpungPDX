from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.record_merger import RecordMerger
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_subsection_6_dismissed():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        disposition=Dispositions.DISMISSED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert isinstance(charges[0].charge_type, DismissedCharge)
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        type_eligibility.reason == "Dismissed Criminal Charge – Dismissals are generally eligible under 137.225(1)(d)"
    )


def test_subsection_6_163165():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Assault in the third degree",
        statute="163.165",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert isinstance(charges[0].charge_type, FelonyClassC)
    assert isinstance(charges[1].charge_type, Subsection6)
    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Felony Class C – Eligible under 137.225(1)(b) OR Subsection 6 – Ineligible under 137.225(6)"
    )


def test_subsection_6_163200():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert isinstance(charges[0].charge_type, Subsection6)
    assert isinstance(charges[1].charge_type, MisdemeanorClassA)
    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Subsection 6 – Ineligible under 137.225(6) OR Misdemeanor Class A – Eligible under 137.225(1)(b)"
    )


def test_subsection_6_163575():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0].charge_type, Subsection6)
    assert isinstance(charges[1].charge_type, MisdemeanorClassA)


def test_subsection_6_163205():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the first degree",
        statute="163.205",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0].charge_type, FelonyClassC)
    assert isinstance(charges[1].charge_type, Subsection6)


def test_subsection_6_163145():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminally negligent homicide",
        statute="163.145",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0].charge_type, MisdemeanorClassA)


def test_163575_is_still_subsection_6_if_b_felony():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0].charge_type, Subsection6)
    assert isinstance(charges[1].charge_type, FelonyClassB)  # TODO: Should this be a person felony?


def test_163200_is_still_subsection_6_if_b_felony():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0].charge_type, Subsection6)
    assert isinstance(charges[1].charge_type, FelonyClassB)  # TODO: Should this be a person felony?
