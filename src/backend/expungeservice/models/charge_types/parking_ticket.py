from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class ParkingTicket(Charge):
    """
    This is a civil offense, and it is also a traffic offense.
    """

    type_name: str = "Parking Ticket"

    def _default_type_eligibility(self):
        if self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        elif self.acquitted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")

    def blocks_other_charges(self):
        return False
