from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class FelonyClassA(ChargeType):
    type_name: str = "Felony Class A"
    expungement_rules: str = (
        """Class A felony convictions generally are omitted from the statute, and are ineligible, unless that Class A Felony was related to the Manufacturing/Delivery/Possession of Marijuana.
Class A felony dismissals are always eligible under 137.225(5)(a).
"""
    )
    severity_level: str = "Felony Class A"

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
