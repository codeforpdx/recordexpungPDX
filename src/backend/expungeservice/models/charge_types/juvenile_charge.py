from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class JuvenileCharge(Charge):
    type_name: str = "Juvenile"

    def _type_eligibility(self):
        return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Potentially eligible under 419A.262")

    def blocks_other_charges(self):
        return False
