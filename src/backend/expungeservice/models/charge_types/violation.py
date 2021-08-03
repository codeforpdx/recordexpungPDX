from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class Violation(ChargeType):
    type_name: str = "Violation"
    expungement_rules: str = """Violations are eligible under ORS 137.225(5)(c) for convictions and 137.225(1)(b) for dismissals.
Examples include Fare Violation, Minor in Possession of Alcohol, Failure to Send or Maintain a Child in School.
However, traffic violations are ineligible under (7)(a).
Moreover, certain civil matters are not considered violations and are thus not eligible, namely Extradition.
"""
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)"
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(c)")
