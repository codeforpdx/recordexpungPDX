from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class UnclassifiedCharge(ChargeType):
    type_name: str = "Unclassified"
    expungement_rules: str = (
        """RecordSponge was not able to read this charge based on the information provided in the online records, and is therefore unable to determine its eligibility for expungement. Furthermore, if the conviction date was within the last ten years, your expungement analysis for your other cases may not be correct."""
    )
    blocks_other_charges: bool = False

    def type_eligibility(self, disposition):
        return TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Unrecognized Charge : Further Analysis Needed"
        )
