import unittest

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory


class TestJuvenileCharge(unittest.TestCase):

    def test_juvenile_charge(self):
        case = CaseFactory.create(type_status=['Juvenile Delinquency: Misdemeanor', 'Closed'])
        juvenile_charge = ChargeFactory.create(case=case)

        assert juvenile_charge.__class__.__name__ == 'JuvenileCharge'
        assert juvenile_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert juvenile_charge.expungement_result.type_eligibility.reason == 'Juvenile Charge : Needs further analysis'
