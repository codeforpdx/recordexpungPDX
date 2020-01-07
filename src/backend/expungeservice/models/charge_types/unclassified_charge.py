from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class UnclassifiedCharge(Charge):
    def _default_type_eligibility(self):
        return TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Unrecognized Charge : Further Analysis Needed"
        )
