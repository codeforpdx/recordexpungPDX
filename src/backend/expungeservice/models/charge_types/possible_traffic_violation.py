from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class PossibleTrafficViolation(ChargeType):
    type_name: str = "Possible Traffic Violation"
    expungement_rules: str = """Violations and misdemeanors reduced to violations in Multnomah County may be considered traffic violations that have insufficient identifying information in OECI. Traffic violation convictions are ineligible under 137.225(7)(a). Other violation or reduced-to-violation convictions are generally eligible however, and if this charge is not traffic-related then the user should Enable Editing to update the charge type to Violation or ReducedToViolation."""
    blocks_other_charges: bool = False
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS,
                reason="Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge.",
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, 
                reason="Either ineligible under 137.225(7)(a) or eligible under 137.225(5)(c)"
            )
        else:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS,
                reason="A possibly-traffic-related violation with indeterminate disposition needs more information to determine eligibility.",
            )

    def hidden_in_record_summary(self, disposition):
        return False
