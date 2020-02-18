from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestSingleChargeConvictionsFelonyClassC(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)

    # TODO: what is this test name?
    def test_misdemeanor_164055(self):
        self.charge_dict["name"] = "Theft in the first degree"
        self.charge_dict["statute"] = "164.055"
        self.charge_dict["level"] = "Felony Class C"
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, FelonyClassC)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
