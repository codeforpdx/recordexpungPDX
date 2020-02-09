from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class FelonyClassB(Charge):
    type_name: str = "Felony Class B"
    expungement_rules: str = (
"""
Applicable subsections: 137.225(5)(a) for convictions; 137.225(5)(a) for dismissals; 137.225(5)(b) provides an additional positive criterion for convictions.

Class B felony dismissals are always eligible under 137.225(5)(a)

Class B felony convictions are generally eligible but subject to additional restrictions compared to other charge types, as listed in 137.225(5)(a).

The extra restrictions are:
 * An extended time restriction: the class B felony is ineligible until 20 years after its date of conviction.
 * The class B felony is ineligible if the person has been arrested or convicted for any crime, other than a traffic violation, following the date of the class B felony conviction.
 * If the charge is also classified as a [Person Crime](manual/charge-types#personcrime) it is ineligible.

If a class B felony is eligible under any other subsection of the statute, that eligibility takes precedences and the extra restrictions here are ignored. The alternate positive criteria that can apply to B felonies are:
 * If the class B felony can be classified as (verify these have valid instances) [Subsection12](manual/charge-types#subsection12), or [Subsection6](manual/charge-types#subsection6).
 * or, If the Class B felony is punishable as a misdemeanor, it is eligible under 137.225(5)(b).
"""
)

    def _default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(1)(b)")
        else:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Further Analysis Needed")
