from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class FelonyClassB(ChargeType):
    type_name: str = "Felony Class B"
    expungement_rules: Any = """Class B felony convictions are generally eligible under ORS 137.225(1)(b). Class B felony dismissals are always eligible under 137.225(1)(d)."""
    severity_level: str = "Felony Class B"

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Convictions that fulfill the conditions of 137.225(1)(b) are eligible",
            )
