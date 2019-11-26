import weakref
from dataclasses import dataclass, InitVar, field

from datetime import date as date_class, datetime
from typing import Optional

from dateutil.relativedelta import relativedelta

from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import ExpungementResult, TimeEligibility, EligibilityStatus

@dataclass
class Charge:
    name: str
    statute: str
    level: str
    date: date_class
    disposition: Optional[Disposition]
    expungement_result: ExpungementResult = field(init=False)
    _chapter: Optional[str]
    _section: str
    _case: weakref.ref

    def __post_init__(self):
        type_eligibility = self._default_type_eligibility()
        self.expungement_result = ExpungementResult(type_eligibility=type_eligibility, time_eligibility=None)

    def _default_type_eligibility(self):
        raise NotImplementedError

    def case(self):
        return self._case

    def acquitted(self):
        return self.disposition and self.disposition.ruling[0:9].lower() != 'convicted'

    def __convicted(self):
        return not self.acquitted()

    def recent_conviction(self):
        ten_years_ago = (date_class.today() + relativedelta(years=-10))
        if self.__convicted():
            return self.disposition.date > ten_years_ago # type: ignore
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
