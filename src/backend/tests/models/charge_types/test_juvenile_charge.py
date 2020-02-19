from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge

from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_juvenile_charge():
    case = CaseFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    juvenile_charge = ChargeFactory.create(case=case, disposition=Dispositions.DISMISSED)

    assert isinstance(juvenile_charge, JuvenileCharge)
    assert juvenile_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert juvenile_charge.expungement_result.type_eligibility.reason == "Potentially eligible under 419A.262"
