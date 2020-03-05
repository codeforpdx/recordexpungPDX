from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class ManufactureDelivery(Charge):
    type_name: str = "Manufacture/Delivery"

    expungement_rules: str = (
        """Manufacture/Delivery is possibly eligible if it pertains to marijuana, under statute 137.226.
Otherwise, it follows the normal eligibility rules for charge level and is typically a Class A or Class B Felony.
It might be a marijuana charge if the charge is for schedule 1, or if the schedule is not specified in the charge name. If it's schedule 2, we can conclude that it's not a marijuana charge.
The charge type is most easily idenfiable by name, so we check the presence of either of the following in the charge name (lowercase): "delivery", "manu/del".
If it's not a marijuana charge, This charge type may or may not have time eligibility under the Class B Felony rule. Because it's simpler to determine time eligibility for a B felony, we instruct the user to determine this information manually:
A Class B Felony that meets no other eligibility criteria will become eligible only after 20 years, and only if the person has no subsequent charges, other than traffic violations.
A dismissed Manufacture/Delivery charge is eligible under 137.225(1)(b).
"""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="This may be eligible if it is a charge for marijuana, under 137.226. See additional legal details.")
        else:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Possibly eligible. See additional legal details.")
