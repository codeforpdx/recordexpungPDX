from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class SevereCharge(Charge):
    type_name: str = "Severe Charge"
    expungement_rules: str = (
        """Charges that are harsher than Class A Felonies in severity: namely, murder and treason."""
    )

    def _type_eligibility(self):
        if self.dismissed():
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
