import weakref

from datetime import datetime
from datetime import date as date_class
from dateutil.relativedelta import relativedelta
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import ExpungementResult


class BaseCharge:

    def __init__(self, case, name, statute, level, date, section, disposition=Disposition()):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.disposition = disposition
        self.expungement_result = ExpungementResult()
        self._section = section
        self._case = weakref.ref(case)

    def case(self):
        return self._case

    def motor_vehicle_violation(self):
        return False

    def acquitted(self):
        if self.disposition.ruling:
            return self.disposition.ruling[0:9] != 'Convicted'

    def recent_conviction(self):
        ten_years_ago = (date_class.today() + relativedelta(years=-10))
        return not self.acquitted() and self.disposition.date > ten_years_ago

    def recent_acquittal(self):
        three_years_ago = (date_class.today() + relativedelta(years=-3))
        return self.acquitted() and self.date > three_years_ago

    def set_time_ineligible(self, reason, date_of_eligibility):
        self.expungement_result.time_eligibility = False
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = date_of_eligibility

    def set_time_eligible(self, reason=''):
        self.expungement_result.time_eligibility = True
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = None
