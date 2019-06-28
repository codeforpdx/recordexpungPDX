import re
import weakref

from datetime import datetime
from datetime import date as date_class
from dateutil.relativedelta import relativedelta
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import ExpungementResult


class Charge:

    def __init__(self, case, name, statute, level, date):
        self._type = None
        self.name = name
        self.statute = Charge.__strip_non_alphanumeric_chars(statute)
        self.level = level
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.disposition = Disposition()
        self.expungement_result = ExpungementResult()
        self._section = Charge.__set_section(statute)
        self._case = weakref.ref(case)

    def case(self):
        return self._case

    @property
    def type(self):
        if self._type:
            return self._type
        else:
            self._set_type()
            return self._type

    def _set_type(self):
        self._set_type_by_statute()
        if not self._type:
            self._set_type_by_level()

    def _set_type_by_statute(self):
        self._marijuana_ineligible()
        self._list_b()
        self._crime_against_person()
        self._traffic_crime()
        self._parking_ticket()
        self._schedule_1_pcs()

    def _set_type_by_level(self):
        self._non_traffic_violation()
        self._misdemeanor()
        self._felony_class_c()
        self._felony_class_b()
        self._felony_class_a()

    def acquitted(self):
        return self.disposition.ruling[0:9] != 'Convicted'

    def recent_conviction(self):
        ten_years_ago = (date_class.today() + relativedelta(years=-10))
        return not self.acquitted() and self.disposition.date > ten_years_ago

    def recent_acquittal(self):
        three_years_ago = (date_class.today() + relativedelta(years=-3))
        return self.acquitted() and self.date > three_years_ago

    def motor_vehicle_violation(self):
        return self.type == 'Parking ticket' or self.type == '800 Level Traffic crime'

    def _marijuana_ineligible(self):
        ineligible_statutes = ['475B359', '475B367', '475B371', '167262']
        if self.statute == '475B3493C' or self._section in ineligible_statutes:
            self._type = 'Marijuana Ineligible'

    def _list_b(self):
        ineligible_statutes = ['163200', '163205', '163575', '163535', '163175', '163275', '162165', '163525', '164405',
                               '164395', '162185', '166220', '163225', '163165']
        if self._section in ineligible_statutes:
            self._type = 'List B'

    def _crime_against_person(self):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        if self._section.isdigit() and any(int(self._section) in statute_range for statute_range in statute_ranges):
            self._type = 'Crime against person'

    def _traffic_crime(self):
        statute_range = range(801, 826)
        if self.statute[0:3].isdigit() and int(self.statute[0:3]) in statute_range:
            self._type = '800 Level Traffic crime'

    def _parking_ticket(self):
        statute_range = range(1, 100)
        if self.statute.isdigit() and int(self.statute) in statute_range:
            self._type = 'Parking ticket'

    def _schedule_1_pcs(self):
        if self._section in ['475854', '475874', '475884', '475894']:
            self._type = 'Schedule 1 PCS'

    def _non_traffic_violation(self):
        if 'Violation' in self.level:
            self._type = 'Non-Traffic Violation'

    def _misdemeanor(self):
        if 'Misdemeanor' in self.level:
            self._type = 'Misdemeanor'

    def _felony_class_c(self):
        if self.level == 'Felony Class C':
            self._type = 'Felony Class C'

    def _felony_class_b(self):
        if self.level == 'Felony Class B':
            self._type = 'Felony Class B'

    def _felony_class_a(self):
        if self.level == 'Felony Class A':
            self._type = 'Felony Class A'

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

    @staticmethod
    def __set_section(statute):
        statute = Charge.__strip_non_alphanumeric_chars(statute)
        if len(statute) < 6:
            return ''
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
