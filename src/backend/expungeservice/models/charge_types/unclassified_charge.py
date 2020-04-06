from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class UnclassifiedCharge(Charge):
    type_name: str = "Unclassified"
    expungement_rules: str = (
        """RecordSponge was not able to read this charge based on the information provided in the online records, and is therefore unable to determine its eligibility for expungement. Furthermore, if the conviction date was within the last ten years, your expungement analysis for your other cases may not be correct."""
    )

    def _type_eligibility(self):
        return TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Unrecognized Charge : Further Analysis Needed"
        )

    def blocks_other_charges(self):
        return False
