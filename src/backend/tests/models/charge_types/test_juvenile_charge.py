from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge

from tests.factories.case_factory import CaseSummaryFactory
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_juvenile_charge_dismissed():
    case = CaseSummaryFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    juvenile_charge = ChargeFactory.create(
        case_number=case.case_number, disposition=Dispositions.DISMISSED, violation_type=case.violation_type
    )

    assert isinstance(juvenile_charge.charge_type, JuvenileCharge)
    assert juvenile_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert juvenile_charge.type_eligibility.reason == "Potentially eligible under 419A.262"


def test_juvenile_charge_convicted():
    case = CaseSummaryFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    juvenile_charge = ChargeFactory.create(
        case_number=case.case_number, disposition=Dispositions.CONVICTED, violation_type=case.violation_type
    )

    assert isinstance(juvenile_charge.charge_type, JuvenileCharge)
    assert juvenile_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert juvenile_charge.type_eligibility.reason == "Potentially eligible under 419A.262"


def test_juvenile_charge_no_disposition():
    case = CaseSummaryFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    juvenile_charge = ChargeFactory.create(
        case_number=case.case_number, disposition=DispositionCreator.empty(), violation_type=case.violation_type
    )

    assert isinstance(juvenile_charge.charge_type, JuvenileCharge)
    assert juvenile_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert juvenile_charge.type_eligibility.reason == "Potentially eligible under 419A.262"


def test_juvenile_charge_unrecognized():
    case = CaseSummaryFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    juvenile_charge = ChargeFactory.create(
        case_number=case.case_number,
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert isinstance(juvenile_charge.charge_type, JuvenileCharge)
    assert juvenile_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert juvenile_charge.type_eligibility.reason == "Potentially eligible under 419A.262"
