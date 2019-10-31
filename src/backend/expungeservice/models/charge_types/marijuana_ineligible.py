from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus

class MarijuanaIneligible(BaseCharge):

    def __init__(self, **kwargs):
        super(MarijuanaIneligible, self).__init__(**kwargs)

    def default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)')
        else:
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason = 'Ineligible under 137.226')
