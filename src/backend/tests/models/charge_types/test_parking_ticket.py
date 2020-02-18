from datetime import date as date_class

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.parking_ticket import ParkingTicket

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestParkingTicket(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict = ChargeFactory.default_dict()
        case = CaseFactory.create(type_status=["Municipal Parking", "Closed"])
        self.charge_dict["statute"] = "109"
        self.charge_dict["case"] = case
        self.charge_dict["level"] = "Violation Unclassified"

    def test_parking_ticket_conviction(self):
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"

    def test_parking_ticket_dismissal(self):
        self.charge_dict["disposition"] = Dispositions.DISMISSED
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"

    def test_parking_ticket_no_disposition(self):
        self.charge_dict["disposition"] = None
        self.charge_dict["date"] = date_class(1901, 1, 1)
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.type_eligibility.reason
            == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
        )

    def test_parking_ticket_unrecognized_disposition(self):
        self.charge_dict["disposition"] = Dispositions.UNRECOGNIZED_DISPOSITION
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.type_eligibility.reason
            == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
        )
