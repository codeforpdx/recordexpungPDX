from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class Violation(Charge):
    type_name: str = "Violation"
    expungement_rules: str = """Violation convictions are eligible under ORS 137.225(5)(d).
Examples include Fare Violation, Minor in Possession of Alcohol, Failure to Send or Maintain a Child in School.
However, traffic violations are ineligible under (7)(a).
Moreover, certain civil matters are not considered violations and are thus not eligible: Contempt of Court, Extradition.
Dismissed violations are ineligible because they are omitted from the expungement statute."""

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Dismissed violations are ineligible by omission from statute"
            )
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(d)")
