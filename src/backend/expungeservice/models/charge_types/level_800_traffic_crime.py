from expungeservice.models.charge_types.base_charge import BaseCharge


class Level800TrafficCrime(BaseCharge):

    def __init__(self, **kwargs):
        super(Level800TrafficCrime, self).__init__(**kwargs)
        if self._expungeable(**kwargs):
            self.expungement_result.set_type_eligibility(True)
            self.expungement_result.set_reason('Eligible under 137.225(1)(b)')
        else:
            self.expungement_result.set_type_eligibility(False)
            self.expungement_result.set_reason('Ineligible under 137.225(5)')

    def skip_analysis(self):
        if self.expungement_result.type_eligibility is True:
            return False
        else:
            return True

    def _expungeable(self, **kwargs):
        return 'misdemeanor' in kwargs['level'].lower() or 'felony' in kwargs['level'].lower()
