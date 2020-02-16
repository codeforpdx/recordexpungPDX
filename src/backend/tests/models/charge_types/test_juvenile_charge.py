import unittest

from datetime import date

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.disposition import Disposition

from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestJuvenileCharge(unittest.TestCase):
    def test_juvenile_charge(self):
        case = CaseFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
        juvenile_charge = ChargeFactory.create(
            case=case, disposition=Disposition(ruling="Acquitted", date=date(2001, 1, 1))
        )

        assert juvenile_charge.__class__.__name__ == "JuvenileCharge"
        assert juvenile_charge.type_name == "Juvenile"
        assert juvenile_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert juvenile_charge.expungement_result.type_eligibility.reason == "Potentially eligible under 419A.262"
