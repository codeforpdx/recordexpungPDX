from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class Misdemeanor(ChargeType):
    type_name: str = "Misdemeanor"
    expungement_rules: str = """Convictions for misdemeanors are generally eligible under ORS 137.225(5)(b).
Exceptions include convictions related to sex, child and elder abuse, and driving, including DUII

Dismissals for misdemeanors are generally eligible under ORS 137.225(1)(b). Exceptions include cases dismissed due to successful completion of DUII diversion."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(b)")
        else:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Misdemeanors are always eligible under 137.225(5)(b) for convictions, or 137.225(1)(b) for dismissals",
            )
