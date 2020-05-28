from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class ReducedToViolation(ChargeType):
    type_name: str = "Reduced to Violation"
    expungement_rules: str = """A criminal charge may sometimes be reduced to a violation, most often in community courts. Violations are eligible under 137.225(5)(d) if convicted, but are typically ineligible if dismissed, by omission. However a reduced charge that is dismissed will usually be accepted as eligible in most courts, as it is still considered a criminal charge and is thus eligible under 137.225(1)(b).
    A charge is recognizable as reduced to violation if its level is Violation, and it contains "reduced" in the charge name."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE, reason="Dismissed criminal charge eligible under 137.225(1)(b)"
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(d)")
        else:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Reduced Violations are always eligible under 137.225(5)(d) for convictions, or 137.225(1)(b) for dismissals",
            )
