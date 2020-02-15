from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class TrafficViolation(Charge):
    type_name: str = "Traffic Violation"

    def _default_type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
        else:
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")

    def blocks_other_charges(self):
        return False

    def hidden_in_record_summary(self):
        return True
