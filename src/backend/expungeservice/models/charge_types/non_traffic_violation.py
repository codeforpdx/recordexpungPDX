from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class NonTrafficViolation(BaseCharge):

    def __init__(self, **kwargs):
        super(NonTrafficViolation, self).__init__(**kwargs)

    def default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)')
        else:
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(5)(d)')
