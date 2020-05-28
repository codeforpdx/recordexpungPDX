from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class TrafficOffense(ChargeType):
    type_name: str = "Traffic Offense"
    expungement_rules: str = (
        """A conviction for a State or municipal traffic offense is not eligible for expungement. Common convictions under this category include Driving While Suspended/Revoked, Possession of a Stolen Vehicle, Driving Under the Influence of Intoxicants, and Failure to Perform Duties of a Driver."""
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
