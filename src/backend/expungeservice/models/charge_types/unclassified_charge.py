from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus

class UnclassifiedCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(UnclassifiedCharge, self).__init__(**kwargs)
        if self.acquitted():
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)'))
        else:
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason = 'Examine'))
