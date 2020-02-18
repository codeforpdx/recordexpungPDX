from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class Schedule1PCS(Charge):
    type_name: str = "Schedule 1 PCS"

    def _type_eligibility(self):
        if self.dismissed():
            # TODO: Are violation dismissals for a PCS actually eligible? This does not appear to be the case.
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(c)")
