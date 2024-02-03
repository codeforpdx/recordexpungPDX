from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class LesserChargeEligible(ChargeType):
    type_name: str = "Lesser Charge, Eligible"
    expungement_rules: str = """A conviction that has been dismissed due to a reduction to a lesser charge is eligible if and only if the new charge is eligible."""

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.ELIGIBLE,
            reason="Reduced to another charge; eligible because the new charge is eligible.",
        )

@dataclass(frozen=True)
class LesserChargeIneligible(ChargeType):
    type_name: str = "Lesser Charge, Ineligible"
    expungement_rules: str = """A conviction that has been dismissed due to a reduction to a lesser charge is eligible if and only if the new charge is eligible."""

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.INELIGIBLE,
            reason="Reduced to another charge; ineligible because the new charge is ineligible.",
        )
