from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class ParkingTicket(Charge):
    """
    This is a civil offense, and it is also a traffic offense.
    """

    type_name: str = "Parking Ticket"
    expungement_rules: str = (
        """Parking Tickets are not eligible. ORS 137.225(7)(a) specifically prohibits expungement of convicted traffic offenses. No other section specifically allows for parking offenses to be eligible."""
    )
    blocks_other_charges: bool = False

    def _type_eligibility(self):
        if self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        elif self.dismissed():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
        elif not self.disposition or self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)",
            )

    def hidden_in_record_summary(self):
        return True
