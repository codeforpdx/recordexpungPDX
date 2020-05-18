from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class TrafficViolation(Charge):
    type_name: str = "Traffic Violation"
    expungement_rules: str = (
        """Convictions for traffic-related offenses are not eligible for expungement under ORS 137.225(7)(a). This includes Violations, Misdemeanors, and Felonies. Traffic-related charges include Reckless Driving, Driving While Suspended, DUII, Failure to Perform Duties of a Driver, Giving False Information to a Police Officer (when in a car), Fleeing/Attempting to Elude a Police Officer, Possession of a Stolen Vehicle
Notably, Unauthorized Use of a Vehicle is not considered a traffic offense.
Dismissed traffic-related Violations are not eligible for expungement
HOWEVER, dismissed traffic-related Misdemeanors and Felonies, like all dismissed Misdemeanors and Felonies, ARE eligible for expungement."""
    )
    blocks_other_charges: bool = False

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Dismissed violations are ineligible by omission from statute"
            )
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        else:
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)",
            )

    def hidden_in_record_summary(self):
        return True
