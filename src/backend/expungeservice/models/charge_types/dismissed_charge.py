from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class DismissedCharge(ChargeType):
    type_name: str = "Dismissed Criminal Charge"
    expungement_rules: str = """Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.
       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection."""

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.ELIGIBLE, reason="Dismissals are generally eligible under 137.225(1)(d)",
        )
