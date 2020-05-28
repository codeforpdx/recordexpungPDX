from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class ParkingTicket(ChargeType):
    """
    This is a civil offense, and it is also a traffic offense.
    """

    type_name: str = "Parking Ticket"
    expungement_rules: str = (
        """Parking Tickets are not eligible. ORS 137.225(7)(a) specifically prohibits expungement of convicted traffic offenses. No other section specifically allows for parking offenses to be eligible."""
    )
    blocks_other_charges: bool = False

    def type_eligibility(self, disposition):
        if ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        elif ChargeUtil.dismissed(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
        elif disposition.status in [DispositionStatus.UNRECOGNIZED, DispositionStatus.UNKNOWN]:
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)",
            )

    def hidden_in_record_summary(self):
        return True
