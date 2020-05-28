from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class Subsection6(ChargeType):
    type_name: str = "Subsection 6"

    expungement_rules: str = (
        """Subsection (6) names five felony statutes that have specific circumstances of the case under which they are ineligible.
However, two of the statutes named -- 163.165(1)(h) (Assault in the third degree)
This subsection also specifies conditions under which [SexCrimes](#SexCrime) are eligible or ineligible.
The three remaining specifications in the statute are:
 * 163.200 (Criminal mistreatment II) is ineligible if the victim at the time of the crime was 65 years of age or older; otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.205 (Criminal mistreatment I) is ineligible if the victim at the time of the crime was 65 years of age or older or a minor; otherwise eligible as a [Class C Felony](#FelonyClassC).
 * 163.575 (Endangering the welfare of a minor) (1)(a) is ineligible when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions); otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.145 (Criminally negligent homicide) is ineligible when that offense was punishable as a Class C felony."""
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(6)",)
