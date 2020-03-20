from datetime import date as date_class
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory
from tests.models.test_charge import Dispositions


def test_contempt_of_court_dismissed():
    case = CaseFactory.create(type_status=["Contempt of Court", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33",
        level="N/A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_convicted():
    case = CaseFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33065",
        level="N/A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_no_disposition():
    case = CaseFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33015",
        level="misdemeanor",
        date=date_class(1901, 1, 1),
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_unrecognized_disposition():
    case = CaseFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33055",
        level="violation",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"
