from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestSingleChargeConvictionsNonTrafficViolation(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict["disposition"] = Dispositions.CONVICTED

    def test_non_traffic_violation(self):
        self.charge_dict["name"] = "Viol Treatment"
        self.charge_dict["statute"] = "1615662"
        self.charge_dict["level"] = "Violation Unclassified"
        charge = ChargeFactory.create(**self.charge_dict)
        self.charges.append(charge)

        assert isinstance(charge, NonTrafficViolation)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(d)"
