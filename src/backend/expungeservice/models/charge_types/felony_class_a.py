from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class FelonyClassA(Charge):
    type_name: str = "Felony Class A"
    expungement_rules: str = (
        """Class A felony convictions generally are omitted from the statute, and are ineligible, unless that Class A Felony was related to the Manufacturing/Delivery/Possession of Marijuana.
Class A felony dismissals are always eligible under 137.225(5)(a).
"""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
