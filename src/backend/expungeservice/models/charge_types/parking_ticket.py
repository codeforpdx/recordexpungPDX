from expungeservice.models.charge_types.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class ParkingTicket(Charge):

    def _default_type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='Ineligible under 137.225(5)')

    def skip_analysis(self):
        return True
