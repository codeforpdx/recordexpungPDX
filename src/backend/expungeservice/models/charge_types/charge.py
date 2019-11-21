import weakref

from datetime import datetime
from datetime import date as date_class
from dateutil.relativedelta import relativedelta
from expungeservice.models.expungement_result import ExpungementResult, TimeEligibility, EligibilityStatus


class Charge:

    def __init__(self, case, name, statute, level, date, chapter, section, disposition=None):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.disposition = disposition
        type_eligibility = self._default_type_eligibility()
        self.expungement_result = ExpungementResult(type_eligibility=type_eligibility, time_eligibility=None)
        self._chapter = chapter
        self._section = section
        self._case = weakref.ref(case)

    def _default_type_eligibility(self):
        raise NotImplementedError

    def case(self):
        return self._case

    def acquitted(self):
        return self.disposition and self.disposition.ruling[0:9].lower() != 'convicted'

    def convicted(self):
        return self.disposition and not self.acquitted()

    def recent_conviction(self):
        ten_years_ago = (date_class.today() + relativedelta(years=-10))
        if self.convicted():
            return self.disposition.date > ten_years_ago
        else:
            return False

    def recent_acquittal(self):
        three_years_ago = (date_class.today() + relativedelta(years=-3))
        return self.acquitted() and self.date > three_years_ago

    def skip_analysis(self):
        return False

    def set_time_ineligible(self, reason, date_of_eligibility):
        status = self.expungement_result.type_eligibility.status
        if status == EligibilityStatus.ELIGIBLE or status == EligibilityStatus.NEEDS_MORE_ANALYSIS:
            date_will_be_eligible = date_of_eligibility
        else:
            date_will_be_eligible = None
        time_eligibility = TimeEligibility(status=False, reason=reason, date_will_be_eligible=date_will_be_eligible)
        self.expungement_result.time_eligibility = time_eligibility

    def set_time_eligible(self, reason=''):
        time_eligibility = TimeEligibility(status=True, reason=reason, date_will_be_eligible=None)
        self.expungement_result.time_eligibility = time_eligibility
