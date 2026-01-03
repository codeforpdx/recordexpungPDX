from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.expungement_result import EligibilityStatus
from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory
from tests.models.test_charge import Dispositions


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

    assert isinstance(charge.charge_type, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_contempt_of_court_convicted():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33065",
        level="N/A",
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_contempt_of_court_no_disposition():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33015",
        level="misdemeanor",
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_contempt_of_court_unrecognized_disposition():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="contempt of court",
        statute="33055",
        level="violation",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, ContemptOfCourt)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
