from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class ParkingTicket(Charge):
    type_name: str = "Parking Ticket"

    def _default_type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(5)")

    def skip_analysis(self):
        return True
