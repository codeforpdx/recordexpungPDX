from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class ContemptOfCourt(ChargeType):
    type_name: str = "Contempt of Court"
    expungement_rules: Any = (
        """The statute was updated as of Jan 1, 2022 to name Contempt of Court as eligible under subsection 137.225(5)(e)."""
    )

    blocks_other_charges: bool = False
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.225(5)(e) for convictions or under 137.225(1)(b) for dismissals")
