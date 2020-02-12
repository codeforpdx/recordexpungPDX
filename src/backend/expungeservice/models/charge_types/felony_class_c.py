from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class FelonyClassC(Charge):
    type_name: str = "Felony Class C"
    expungement_rules: str = (
        """
Applicable subsections: 137.225(5)(b) for convictions; 137.225(1)(b) for dismissals.
Class C felony dismissals are always eligible under 137.225(1)(b)
Class C felony convictions are generally eligible.

The possible extra restrictions are:
 * Criminally negligent homicide.
 * Sex crimes.
"""
    )

    def _default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)")
        else:
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(b)")
