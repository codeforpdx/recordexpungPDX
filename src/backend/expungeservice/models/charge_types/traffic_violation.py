from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class TrafficViolation(ChargeType):
    type_name: str = "Traffic Violation"
    expungement_rules: str = """Convictions for traffic-related offenses are not eligible for expungement under ORS 137.225(7)(a). This includes Violations, Misdemeanors, and Felonies.
            Dismissed traffic violations are also ineligible, because Violations generally are omitted from the statute.
            However, dismissed traffic-related Misdemeanors and Felonies, like all dismissed Misdemeanors and Felonies, ARE eligible for expungement."""
    blocks_other_charges: bool = False

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Dismissed violations are ineligible by omission from statute"
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        else:
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)",
            )

    def hidden_in_record_summary(self):
        return True
