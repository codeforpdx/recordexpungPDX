import re
import weakref

from datetime import datetime
from datetime import date as date_class
from dateutil.relativedelta import relativedelta
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import ExpungementResult


class Charge:

    def __init__(self, case, name, statute, level, date):
        self.name = name
        self.statute = Charge.__strip_non_alphanumeric_chars(statute)
        self.level = level
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.disposition = Disposition()
        self.expungement_result = ExpungementResult()
        self._case = weakref.ref(case)

    def case(self):
        return self._case

    def acquitted(self):
        return self.disposition.ruling[0:9] != 'Convicted'

    def recent_conviction(self):
        ten_years_ago = (date_class.today() + relativedelta(years=-10))
        return not self.acquitted() and self.disposition.date > ten_years_ago

    def recent_acquittal(self):
        three_years_ago = (date_class.today() + relativedelta(years=-3))
        return self.acquitted() and self.date > three_years_ago

    def traffic_crime(self):
        statute = int(self.statute[0:3])
        statute_range = range(801, 826)
        return statute in statute_range

    def set_time_ineligible(self, reason, date_of_eligibility):
        self.expungement_result.time_eligibility = False
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = date_of_eligibility

    def set_time_eligible(self, reason=''):
        self.expungement_result.time_eligibility = True
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = None

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r'[^a-zA-Z0-9*]', '', statute).upper()
