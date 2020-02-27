from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class ManufactureDelivery(Charge):
    type_name: str = "Manufacture/Delivery"

    expungement_rules: str = (
        """Manu/Delivery is Felony (may be Class A or B) with specific eligibility rules.
The charge type is most easily idenfiable by name, so we check the presence of either of the following in the charge name (lowercase): "delivery", "manu/del".
If the charge is convicted, and if the charge level is Felony Class B, it is type-eligible and follows the time eligibility rules of a Felony Class B (20 years, no subsequent arrests/convictions) 137.225(5)(a)(A)(1).
If the level is Felony Class A, the charge may be a Marijuana charge which would be eligible, so the charge needs more analysis, is possibly eligible under the 10-year rule for convictions.
If the level is Felony Unclassified, it needs more analysis because it may be a Felony Class B. Set the time eligibility to needs more analysis, with the 10 year rule.
A dismissal is eligible under 137.225(1(b).
"""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            if "Felony Class A" in self.level:
                return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="If this is a marijuana conviction, it's eligible under 137.226. Otherwise it's ineligible by omission from statute.")
            elif "Felony Class B" in self.level:
                return TypeEligibility(
                    EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(a) as a Class B Felony, and follows B felony time restrictions. If this is a marijuana-related charge, it is eligible under 137.226 and follows normal time eligibility rules. .",
                )
            else: # (this includes if "Felony Unclassified" in self.level)
                return TypeEligibility(
                    EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Possibly eligible under 137.225(5)(a), if this is a Class B Felony. If so, time eligibility follows the 20-year B felony rule.",
                )
