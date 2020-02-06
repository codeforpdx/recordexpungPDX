import unittest
from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.parking_ticket import ParkingTicket

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory


class TestParkingTicket(unittest.TestCase):
    def setUp(self):
        self.charge_dict = ChargeFactory.build()
        case = CaseFactory.create(type_status=["Municipal Parking", "Closed"])
        self.charge_dict["statute"] = "109"
        self.charge_dict["case"] = case
        self.charge_dict["level"] = "Violation Unclassified"
        last_week = datetime.today() - timedelta(days=7)
        self.convicted = ["Convicted", last_week]
        self.dismissed = ["Dismissed", last_week]

    def test_parking_ticket_conviction(self):
        self.charge_dict["disposition"]=self.convicted
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert charge.skip_analysis()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"

    def test_parking_ticket_dismissal(self):
        self.charge_dict["disposition"]=self.dismissed
        charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(charge, ParkingTicket)
        assert charge.skip_analysis()
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"


