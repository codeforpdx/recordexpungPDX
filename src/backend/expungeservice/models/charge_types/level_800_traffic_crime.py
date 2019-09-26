from expungeservice.models.charge_types.base_charge import BaseCharge


class Level800TrafficCrime(BaseCharge):

    def __init__(self, **kwargs):
        super(Level800TrafficCrime, self).__init__(**kwargs)
        if self._expungeable():
            self.expungement_result.set_type_eligibility(True)
            self.expungement_result.set_reason('Eligible under 137.225(1)(b)')
        else:
            self.expungement_result.set_type_eligibility(False)
            self.expungement_result.set_reason('Ineligible under 137.225(5)')

    def skip_analysis(self):
        if self._affects_time_analysis():
            return False
        else:
            return True

    def _expungeable(self):
        return self.acquitted() and self._affects_time_analysis()

    def _affects_time_analysis(self):
        return 'misdemeanor' in self.level.lower() or 'felony' in self.level.lower()
