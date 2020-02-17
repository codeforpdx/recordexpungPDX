from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class NonTrafficViolation(Charge):
    type_name: str = "Non-traffic Violation"
    expungement_rules: str = """Violations are eligible under ORS 137.225(5)(d).
Examples include Fare Violation, Minor in Possession of Alcohol, Failure to Send or Maintain a Child in School.
However, traffic violations are ineligible under (7)(a).
Moreover, certain matters are not eligible: Contempt of Court, Extradition"""

    def _default_type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)")
        else:
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(d)")
