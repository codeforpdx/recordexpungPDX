from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class MarijuanaIneligible(Charge):
    type_name: str = "Marijuana Ineligible"

    def _default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)")
        else:
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.226")
