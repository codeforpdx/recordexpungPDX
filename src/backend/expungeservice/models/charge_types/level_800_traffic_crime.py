from expungeservice.models.charge_types.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class Level800TrafficCrime(Charge):

    def _default_type_eligibility(self):
        if self._expungeable():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason='Eligible under 137.225(1)(b)')
        else:
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='Ineligible under 137.225(5)')

    def skip_analysis(self):
        if self._affects_time_analysis():
            return False
        else:
            return True

    def _expungeable(self):
        return self.acquitted() and self._affects_time_analysis()

    def _affects_time_analysis(self):
        return 'misdemeanor' in self.level.lower() or 'felony' in self.level.lower()
