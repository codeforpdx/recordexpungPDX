from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class FareViolation(ChargeType):
    type_name: str = "FareViolation"
    expungement_rules: str = """A Fare Violation follows normal eligibility rules of a Violation, even though it typically falls under a statute number that would identify it as a Civil Offense.
Violation convictions are eligible under ORS 137.225(5)(d).
Dismissed violations are ineligible because they are omitted from the expungement statute."""
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Dismissed violations are ineligible by omission from statute"
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(d)")
