from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.helpers.record_merger import RecordMerger
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

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], Misdemeanor)
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"


def test_subsection_6_163165():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Assault in the third degree",
        statute="163.165",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], FelonyClassC)
    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert type_eligibility.reason == "Ineligible under 137.225(6) ⬥ Eligible under 137.225(5)(b)"


def test_subsection_6_163200():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], Misdemeanor)
    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert type_eligibility.reason == "Ineligible under 137.225(6) ⬥ Eligible under 137.225(5)(b)"


def test_subsection_6_163575():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], Misdemeanor)


def test_subsection_6_163205():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the first degree",
        statute="163.205",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], FelonyClassC)


def test_subsection_6_163145():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminally negligent homicide",
        statute="163.145",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], Misdemeanor)


def test_163575_is_still_subsection_6_if_b_felony():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], FelonyClassB)  # TODO: Should this be a person felony?


def test_163200_is_still_subsection_6_if_b_felony():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charges[0], Subsection6)
    assert isinstance(charges[1], FelonyClassB)  # TODO: Should this be a person felony?
