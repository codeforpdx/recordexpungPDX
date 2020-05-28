from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class FelonyClassC(ChargeType):
    type_name: str = "Felony Class C"
    expungement_rules: str = (
        """There are certain types of Class C felony which are generally ineligible, including sex crimes, child
abuse, elder abuse, traffic crimes, and criminally negligent homicide. Other Class C felony convictions are almost
always eligible under 137.225(5)(b).
Class C felony dismissals are always eligible under 137.225(1)(b)."""
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(b)")
        elif disposition.status in [DispositionStatus.UNKNOWN, DispositionStatus.UNRECOGNIZED]:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Eligible under 137.225(5)(b) for convictions or under 137.225(1)(b) for dismissals",
            )  # TODO: Double check
