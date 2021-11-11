from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class ParkingTicket(ChargeType):
    type_name: str = "Parking Ticket"
    expungement_rules: str = """Parking Ticket convictions are not eligible. ORS 137.225(7)(a) specifically prohibits expungement of convicted traffic offenses. Dismissed parking offenses are effectively ineligible at the discretion of the court."""
    blocks_other_charges: bool = False
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        if ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        elif ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Dismissed parking violations are effectively ineligible at the discretion of the court.",
            )

    def hidden_in_record_summary(self, disposition):
        return ChargeUtil.convicted(disposition)
