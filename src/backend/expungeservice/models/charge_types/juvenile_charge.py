from expungeservice.models.charge_types.base_charge import BaseCharge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class JuvenileCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(JuvenileCharge, self).__init__(**kwargs)
        self.expungement_result.set_type_eligibility(
            TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason = 'Juvenile Charge : Needs further analysis'))

    def skip_analysis(self):
        return True
