from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class Subsection6(Charge):
    type_name: str = "Subsection 6"

    expungement_rules: str = (
        """Subsection (6) names five felony statutes that have specific circumstances of the case under which they are ineligible.
However, two of the statutes named -- 163.165(1)(h) (Assault in the third degree) and 163.205 (Criminal mistreatment in the first degree) are also named in subection 12 as eligible. Subsection 12 is interpreted to override other statutes, so in effect this clause of subsection 6 has no effect on eligibility.
This subsection also specifies conditions under which [SexCrimes](#SexCrime) are eligible or ineligible.
The three remaining specifications in the statute are:
 * 163.200 (Criminal mistreatment in the second degree) is ineligible if the victim at the time of the crime was 65 years of age or older; otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.575 (Endangering the welfare of a minor) (1)(a) is ineligible when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions); otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.145 (Criminally negligent homicide) is ineligible when that offense was punishable as a Class C felony.
Applicable subsections: 137.225(6) for convictions; 137.225(1)(b) for dismissals."""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Ineligible under 137.225(6) in certain circumstances.",
            )
