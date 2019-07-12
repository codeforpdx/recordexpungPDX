from expungeservice.models.charge_types.base_charge import BaseCharge


class JuvenileCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(JuvenileCharge, self).__init__(**kwargs)
        self.expungement_result.set_type_eligibility(None)
        self.expungement_result.set_reason('Juvenile Charge : Needs further analysis')

    def skip_analysis(self):
        return True
