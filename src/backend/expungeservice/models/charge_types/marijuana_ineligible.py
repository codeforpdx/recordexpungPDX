from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus

class MarijuanaIneligible(BaseCharge):

    def __init__(self, **kwargs):
        super(MarijuanaIneligible, self).__init__(**kwargs)
        if self.acquitted():
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)'))
        else:
            self.expungement_result.set_type_eligibility(TypeEligibility(EligibilityStatus.INELIGIBLE, reason = 'Ineligible under 137.226'))
