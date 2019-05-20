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
        self._section = Charge.__set_section(Charge.__strip_non_alphanumeric_chars(statute))
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
        statute_range = range(801, 826)

        if self.statute[0:3].isdigit():
            return int(self.statute[0:3]) in statute_range
        else:
            return False

    def marijuana_ineligible(self):
        if self.statute == '475B3493C':
            return True
        else:
            ineligible_statutes = ['475B359', '475B367', '475B371', '167262']
            return self._section in ineligible_statutes

    def list_b(self):
        ineligible_statutes = ['163200', '163205', '163575', '163535', '163175', '163275', '162165', '163525', '164405',
                               '164395', '162185', '166220', '163225', '163165']
        return self._section in ineligible_statutes

    def ineligible_under_137_225_5(self):
        return self._crime_against_person() or self.traffic_crime() or self._felony_class_a()

    def possession_sched_1(self):
        return self._section in ['475854', '475874', '475884', '475894']

    def non_traffic_violation(self):
        return 'Violation' in self.level

    def set_time_ineligible(self, reason, date_of_eligibility):
        self.expungement_result.time_eligibility = False
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = date_of_eligibility

    def set_time_eligible(self, reason=''):
        self.expungement_result.time_eligibility = True
        self.expungement_result.time_eligibility_reason = reason
        self.expungement_result.date_of_eligibility = None

    def _crime_against_person(self):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))

        if self._section.isdigit():
            return any(int(self._section) in statute_range for statute_range in statute_ranges)
        else:
            return False

    def _felony_class_a(self):
        return self.level == 'Felony Class A'

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r'[^a-zA-Z0-9*]', '', statute).upper()

    @staticmethod
    def __set_section(statute):
        if len(statute) < 6:
            return None
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
