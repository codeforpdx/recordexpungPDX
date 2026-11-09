from expungeservice.charge_creator import ChargeCreator
from expungeservice.models.charge import EditStatus
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt, ContemptOfCourtChildSupport
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


def contempt_charge_in(location):
    return ChargeCreator.create(
        "1-1",
        case_number="1",
        name="Contempt of Court",
        statute="33065",
        level="N/A",
        date=Dispositions.CONVICTED.date,
        disposition=Dispositions.CONVICTED,
        violation_type="Contempt of Court",
        location=location,
        balance_due_in_cents=0,
        edit_status=EditStatus.UNCHANGED,
    )


def test_washington_contempt_asks_whether_it_involves_child_support():
    ambiguous_charge, question = contempt_charge_in("Washington")

    assert question.text == "Does this charge involve child support?"
    assert question.options["Yes"].edit == {"charge_type": "ContemptOfCourtChildSupport"}
    assert question.options["No"].edit == {"charge_type": "ContemptOfCourt"}
    assert {type(charge.charge_type) for charge in ambiguous_charge} == {ContemptOfCourtChildSupport, ContemptOfCourt}


def test_contempt_elsewhere_asks_nothing():
    ambiguous_charge, question = contempt_charge_in("Multnomah")

    assert question is None
    assert len(ambiguous_charge) == 1
    assert type(ambiguous_charge[0].charge_type) is ContemptOfCourt


def test_child_support_contempt_is_contempt_with_the_same_eligibility():
    child_support = ContemptOfCourtChildSupport()

    assert isinstance(child_support, ContemptOfCourt)
    assert child_support.type_name == "Contempt of Court - Child Support"
    assert child_support.type_eligibility(Dispositions.CONVICTED) == ContemptOfCourt().type_eligibility(Dispositions.CONVICTED)
