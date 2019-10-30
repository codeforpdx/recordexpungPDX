from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus

class Schedule1PCS(BaseCharge):

    def __init__(self, **kwargs):
        super(Schedule1PCS, self).__init__(**kwargs)
        if self.acquitted():
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)'))
        else:
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(5)(C)'))
