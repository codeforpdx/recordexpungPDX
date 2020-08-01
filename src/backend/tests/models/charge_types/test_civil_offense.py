from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.expungement_result import EligibilityStatus
from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory
from tests.models.test_charge import Dispositions


def test_00_is_not_a_civil_offense():
    charge = ChargeFactory.create(statute="00", level="N/A", disposition=Dispositions.CONVICTED)

    assert not isinstance(charge.charge_type, CivilOffense)


def test_100_is_not_a_civil_offense():
    charge = ChargeFactory.create(statute="100", level="N/A", disposition=Dispositions.CONVICTED)

    assert not isinstance(charge.charge_type, CivilOffense)


def test_99_is_a_civil_offense():
    charge = ChargeFactory.create(statute="99", level="N/A", disposition=Dispositions.CONVICTED)

    assert isinstance(charge.charge_type, CivilOffense)


def test_55_is_a_civil_offense():
    charge = ChargeFactory.create(statute="55", level="N/A", disposition=Dispositions.CONVICTED)

    assert isinstance(charge.charge_type, CivilOffense)


def test_fugitive_complaint():
    charge = ChargeFactory.create(
        statute="0", level="N/A", name="Fugitive Complaint", disposition=Dispositions.CONVICTED
    )
    assert isinstance(charge.charge_type, CivilOffense)


def test_extradition():
    charge = ChargeFactory.create(
        statute="00000336", level="Felony Unclassified", name="FUG/WA", disposition=Dispositions.DISMISSED
    )
    assert isinstance(charge.charge_type, CivilOffense)


def test_contempt_of_court():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="",
        level="N/A",
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, CivilOffense)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_convicted():
    case = CaseSummaryFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33065",
        level="N/A",
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, CivilOffense)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_no_disposition():
    case = CaseSummaryFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33015",
        level="misdemeanor",
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, CivilOffense)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_unrecognized_disposition():
    case = CaseSummaryFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33055",
        level="violation",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, CivilOffense)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"
