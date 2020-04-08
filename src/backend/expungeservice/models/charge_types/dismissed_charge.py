from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class DismissedCharge(Charge):
    type_name: str = "Dismissed Criminal Charge"
    expungement_rules: str = ("""All non-duii criminal charges that are dismissed fall under this charge type.""")

    def _type_eligibility(self):
        return TypeEligibility(
            EligibilityStatus.ELIGIBLE, reason="Dismissals are generally eligible under 137.225(1)(b)",
        )
