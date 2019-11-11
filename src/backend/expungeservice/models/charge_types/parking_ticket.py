from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class ParkingTicket(BaseCharge):

    def __init__(self, **kwargs):
        super(ParkingTicket, self).__init__(**kwargs)

    def default_type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason = 'Ineligible under 137.225(5)')

    def skip_analysis(self):
        return True
