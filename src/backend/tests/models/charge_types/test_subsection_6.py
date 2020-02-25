from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_subsection_6_dismissed():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Criminal mistreatment in the second degree"
    charge_dict["statute"] = "163.200"
    charge_dict["level"] = "Misdemeanor Class A"
    charge_dict["disposition"] = Dispositions.DISMISSED

    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_6_charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    )


def test_subsection_6_163165():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Assault in the third degree"
    charge_dict["statute"] = "163.165"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        subsection_6_charge.expungement_result.type_eligibility.reason
        == "Ineligible under 137.225(6) in certain circumstances."
    )


def test_subsection_6_163200():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Criminal mistreatment in the second degree"
    charge_dict["statute"] = "163.200"
    charge_dict["level"] = "Misdemeanor Class A"
    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, Subsection6)
    assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        subsection_6_charge.expungement_result.type_eligibility.reason
        == "Ineligible under 137.225(6) in certain circumstances."
    )


def test_subsection_6_163575():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Endangering the welfare of a minor"
    charge_dict["statute"] = "163.575"
    charge_dict["level"] = "Misdemeanor Class A"
    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, Subsection6)


def test_subsection_6_does_not_apply_when_felony_class_b():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Criminally negligent homicide"
    charge_dict["statute"] = "163.145"
    charge_dict["level"] = "Felony Class B"
    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, PersonFelonyClassB)


def test_subsection_6_163205():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Criminal mistreatment in the first degree"
    charge_dict["statute"] = "163.205"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_6_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_6_charge, Subsection6)
