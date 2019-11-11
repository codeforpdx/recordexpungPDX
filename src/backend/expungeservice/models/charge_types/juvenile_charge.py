from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class JuvenileCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(JuvenileCharge, self).__init__(**kwargs)

    def default_type_eligibility(self):
        return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason = 'Juvenile Charge : Needs further analysis')

    def skip_analysis(self):
        return True
