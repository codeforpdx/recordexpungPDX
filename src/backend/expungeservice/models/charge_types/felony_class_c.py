from expungeservice.models.charge_types.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class FelonyClassC(Charge):

    def __init__(self, **kwargs):
        super(FelonyClassC, self).__init__(**kwargs)

    def default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(1)(b)')
        else:
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason = 'Eligible under 137.225(5)(b)')