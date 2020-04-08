from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class TrafficOffense(Charge):
    type_name: str = "Traffic Offense"
    expungement_rules: str = (
        """A conviction for a State or municipal traffic offense is not eligible for expungement. Common convictions under this category include Driving While Suspended/Revoked, Possession of a Stolen Vehicle, Driving Under the Influence of Intoxicants, and Failure to Perform Duties of a Driver."""
    )

    def _type_eligibility(self):
        if self.dismissed():
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
