from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt, SevereContemptOfCourt
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.record_merger import RecordMerger
from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory
from tests.models.test_charge import Dispositions


def test_contempt_of_court():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="contempt of court",
        statute="",
        level="N/A",
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    # Contempt of court is now ambiguous - could be regular or severe
    assert len(charges) == 2
    assert isinstance(charges[0].charge_type, ContemptOfCourt)
    assert isinstance(charges[1].charge_type, SevereContemptOfCourt)

    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert "137.225(5)(e)" in type_eligibility.reason or "137.225(1)(b)" in type_eligibility.reason


def test_contempt_of_court_convicted():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="contempt of court",
        statute="33065",
        level="N/A",
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert len(charges) == 2
    assert isinstance(charges[0].charge_type, ContemptOfCourt)
    assert isinstance(charges[1].charge_type, SevereContemptOfCourt)

    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert "137.225(5)(e)" in type_eligibility.reason or "137.225(1)(b)" in type_eligibility.reason


def test_contempt_of_court_no_disposition():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="contempt of court",
        statute="33015",
        level="misdemeanor",
        violation_type=case.violation_type,
    )

    assert len(charges) == 2
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    # Both types are eligible, so merged result is eligible
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_contempt_of_court_unrecognized_disposition():
    case = CaseSummaryFactory.create(type_status=["Contempt of Court", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="contempt of court",
        statute="33055",
        level="violation",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert len(charges) == 2
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    # Both types are eligible regardless of disposition
    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
