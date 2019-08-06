import unittest

from tests.factories.charge_factory import ChargeFactory


class TestParkingTicket(unittest.TestCase):

    def setUp(self):
        self.parking_ticket = ChargeFactory.create(name='Loading Zone',
                                                   statute='29',
                                                   level='Violation Unclassified',
                                                   disposition=['Convicted', '5/5/1999'])

    def test_parking_violation(self):
        assert self.parking_ticket.expungement_result.type_eligibility is False
        assert self.parking_ticket.expungement_result.type_eligibility_reason == 'Ineligible under 137.225(5)'

    def test_parking_tickets_skip_analysis(self):
        assert self.parking_ticket.skip_analysis() is True
