from expungeservice.models.charge_types.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class JuvenileCharge(Charge):

    def _default_type_eligibility(self):
        return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Juvenile Charge : Needs further analysis')

    def skip_analysis(self):
        return True
