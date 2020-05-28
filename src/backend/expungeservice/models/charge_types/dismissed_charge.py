from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class DismissedCharge(ChargeType):
    type_name: str = "Dismissed Criminal Charge"
    expungement_rules: str = ("""All non-duii criminal charges that are dismissed fall under this charge type.""")

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.ELIGIBLE, reason="Dismissals are generally eligible under 137.225(1)(b)",
        )
