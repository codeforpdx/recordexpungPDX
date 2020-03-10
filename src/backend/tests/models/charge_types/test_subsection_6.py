from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_subsection_6_dismissed():
    subsection_6_charge = ChargeFactory.create(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert subsection_6_charge.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"


def test_subsection_6_163165():
    subsection_6_charge = ChargeFactory.create(
        name="Assault in the third degree",
        statute="163.165",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert subsection_6_charge.type_eligibility.reason == "Ineligible under 137.225(6) in certain circumstances."


def test_subsection_6_163200():
    subsection_6_charge = ChargeFactory.create(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert subsection_6_charge.type_eligibility.reason == "Ineligible under 137.225(6) in certain circumstances."


def test_subsection_6_163575():
    subsection_6_charge = ChargeFactory.create(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)


def test_subsection_6_163205():
    subsection_6_charge = ChargeFactory.create(
        name="Criminal mistreatment in the first degree",
        statute="163.205",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)


def test_subsection_6_163145():
    subsection_6_charge = ChargeFactory.create(
        name="Criminally negligent homicide",
        statute="163.145",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)


def test_163575_is_still_subsection_6_if_b_felony():
    subsection_6_charge = ChargeFactory.create(
        name="Endangering the welfare of a minor",
        statute="163.575",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)


def test_163200_is_still_subsection_6_if_b_felony():
    subsection_6_charge = ChargeFactory.create(
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(subsection_6_charge, Subsection6)
