from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class FareViolation(ChargeType):
    type_name: str = "FareViolation"
    expungement_rules: str = """Trimet-related fare violations are not prosecuted by the county DA and are not problematic for individuals, so we don't file them for expungement."""
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.INELIGIBLE,
            reason="Trimet-related fare violations are not prosecuted by the county DA and are not problematic for individuals, so we don't file them for expungement.",
        )
