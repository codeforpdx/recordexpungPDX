from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class FelonyClassC(Charge):
    type_name: str = "Felony Class C"
    expungement_rules: str = (
        """
Class C felony convictions are almost always eligible under 137.225(5)(b).
Class C felony dismissals are always eligible under 137.225(1)(b)

Class C felonies are lower in our hierarchy of type classifications, so many Class C
felonies are superseded by their designations as other types. For example, if a Class C
felony is a sex crime, its eligibility is first and foremost determined by its sex crime.

Possible edge-case restrictions:
 * Criminally negligent homicide is not eligible if it is classified as a Class C felony, under 137.225(6)(d). This is an edge-case because criminally negligent homicide will almost always be a Class B felony.

Applicable subsections: 137.225(5)(b) for convictions; 137.225(1)(b) for dismissals.
"""
    )

    def _default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)")
        else:
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(b)")
