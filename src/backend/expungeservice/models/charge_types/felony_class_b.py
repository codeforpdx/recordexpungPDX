from expungeservice.models.charge_types.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class FelonyClassB(Charge):

    def _default_type_eligibility(self):
        if self.acquitted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason='Eligible under 137.225(1)(b)')
        else:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed')
