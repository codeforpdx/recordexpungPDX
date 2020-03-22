from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass
class FelonyClassC(Charge):
    type_name: str = "Felony Class C"
    expungement_rules: str = (
        """There are certain types of Class C felony which are generally ineligible, including sex crimes, child
abuse, elder abuse, traffic crimes, and criminally negligent homicide. Other Class C felony convictions are almost
always eligible under 137.225(5)(b).
Class C felony dismissals are always eligible under 137.225(1)(b)."""
    )

    def _type_eligibility(self):
        if self.dismissed():
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(b)")
        elif not self.disposition or self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Eligible under 137.225(5)(b) for convictions or under 137.225(1)(b) for dismissals",
            )
