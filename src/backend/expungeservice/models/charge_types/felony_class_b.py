from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class FelonyClassB(Charge):
    type_name: str = "Felony Class B"
    expungement_rules: str = (
        """Class B felony dismissals are always eligible under 137.225(5)(a).
Class B felony convictions are generally eligible but subject to additional restrictions compared to other charge types, as listed in 137.225(5)(a).
The extra restrictions are:
 * An extended time restriction: the class B felony is ineligible until 20 years after its date of conviction.
 * The class B felony is ineligible if the person has been arrested or convicted for any crime, other than a traffic violation, following the date of the class B felony conviction.
 * If the charge is also classified as a [Person Crime](manual/charge-types#personcrime) it is ineligible.
If a class B felony is eligible under any other subsection of the statute, that eligibility takes precedences and the extra restrictions here are ignored. The alternate positive criteria that can apply to B felonies are:
 * Some class B felonies fall under [Subsection6](#Subsection6) or [Subsection12](#Subsection12), which take precendence over 137.225(5)(a).
 * or, If the class B felony is punishable as a misdemeanor, it is eligible under 137.225(5)(b)."""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Further Analysis Needed")
