from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class UnclassifiedCharge(Charge):
    type_name: str = "Unclassified"

    def _type_eligibility(self):
        return TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Unrecognized Charge : Further Analysis Needed"
        )
