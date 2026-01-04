from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class ContemptOfCourt(ChargeType):
    type_name: str = "Contempt of Court"
    expungement_rules: Any = (
        """Under 137.225(1)(b)(B), a finding of contempt of court for violating an order related to abuse or a person crime requires a 5-year wait period, the same as a Class C Felony."""
    )

    blocks_other_charges: bool = True
    severity_level: str = "Felony Class C"

    def type_eligibility(self, disposition):
        return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(e) for convictions or under 137.225(1)(b) for dismissals")
