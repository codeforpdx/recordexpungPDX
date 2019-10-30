import unittest

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


class TestParkingTicket(unittest.TestCase):

    def build(self, ruling='Convicted'):
        self.parking_ticket = ChargeFactory.create(name='Loading Zone',
                                                   statute='29',
                                                   level='Violation Unclassified',
                                                   disposition=[ruling, '5/5/1999'])

    def test_parking_violation(self):
        self.build()

        assert self.parking_ticket.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert self.parking_ticket.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_parking_tickets_skip_analysis(self):
        self.build()

        assert self.parking_ticket.skip_analysis() is True

    def test_acuitted_tickets_are_not_type_eligible(self):
        self.build(ruling='Dismissed')

        self.parking_ticket.disposition.ruling = 'Dismissed'

        assert self.parking_ticket.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
