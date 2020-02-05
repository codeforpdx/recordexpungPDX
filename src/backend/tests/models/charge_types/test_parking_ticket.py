import unittest

from datetime import datetime, timedelta
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory


class TestTrafficTicket(unittest.TestCase):
    def setUp(self):
        self.charge_kwargs = ChargeFactory.build()
        case = CaseFactory.create(type_status=["Municipal Parking", "Closed"])
        self.charge_kwargs["statute"] = "109"
        self.charge_kwargs["case"] = case
        self.charge_kwargs["level"] = "Violation Unclassified"
        last_week = datetime.today() - timedelta(days=7)
        self.convicted = ["Convicted", last_week]
        self.dismissed = ["Dismissed", last_week]

    def test_parking_ticket_conviction(self):
        self.charge_kwargs["disposition"]=self.convicted
        charge = ChargeFactory.create(**self.charge_kwargs)

        assert charge.__class__.__name__ == "ParkingTicket"
        assert charge.skip_analysis() is True
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"


    def test_acuitted_tickets_are_not_type_eligible(self):
        self.charge_kwargs["disposition"]=self.dismissed
        charge = ChargeFactory.create(**self.charge_kwargs)

        assert charge.__class__.__name__ == "ParkingTicket"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"


