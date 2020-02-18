from datetime import date as date_class

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.parking_ticket import ParkingTicket

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestParkingTicket(ChargeTypeTest):
    def test_parking_ticket_conviction(self):
        charge_dict = {
            "case": CaseFactory.create(type_status=["Municipal Parking", "Closed"]),
            "name": "Unknown",
            "statute": "109",
            "level": "Violation Unclassified",
            "date": date_class(1901, 1, 1),
            "disposition": Dispositions.CONVICTED,
        }
        charge = ChargeFactory.create(**charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"

    def test_parking_ticket_dismissal(self):
        charge_dict = {
            "case": CaseFactory.create(type_status=["Municipal Parking", "Closed"]),
            "name": "Unknown",
            "statute": "109",
            "level": "Violation Unclassified",
            "date": date_class(1901, 1, 1),
            "disposition": Dispositions.DISMISSED,
        }
        charge = ChargeFactory.create(**charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"

    def test_parking_ticket_no_disposition(self):
        charge_dict = {
            "case": CaseFactory.create(type_status=["Municipal Parking", "Closed"]),
            "name": "Unknown",
            "statute": "109",
            "level": "Violation Unclassified",
            "date": date_class(1901, 1, 1),
            "disposition": None,
        }
        charge = ChargeFactory.create(**charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.type_eligibility.reason
            == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
        )

    def test_parking_ticket_unrecognized_disposition(self):
        charge_dict = {
            "case": CaseFactory.create(type_status=["Municipal Parking", "Closed"]),
            "name": "Unknown",
            "statute": "109",
            "level": "Violation Unclassified",
            "date": date_class(1901, 1, 1),
            "disposition": Dispositions.UNRECOGNIZED_DISPOSITION,
        }
        charge = ChargeFactory.create(**charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert not charge.blocks_other_charges()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.type_eligibility.reason
            == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
        )
