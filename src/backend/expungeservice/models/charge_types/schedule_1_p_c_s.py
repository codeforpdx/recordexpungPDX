from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class Schedule1PCS(Charge):
    type_name: str = "Schedule 1 PCS"

    def _type_eligibility(self):
        if self.dismissed():
            if "violation" in self.level.lower():
                return TypeEligibility(
                    EligibilityStatus.INELIGIBLE,
                    reason="Dismissed violations are ineligible by omission from statute"
                )
            else:
                return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(c)")
