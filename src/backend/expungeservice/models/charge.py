import weakref
from dataclasses import dataclass, InitVar, field

from datetime import date as date_class, datetime
from typing import Optional

from dateutil.relativedelta import relativedelta

from expungeservice.models.disposition import Disposition, DispositionStatus
from expungeservice.models.expungement_result import (
    ExpungementResult,
    TimeEligibility,
    TypeEligibility,
    EligibilityStatus,
)


@dataclass(eq=False)
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
    type_name: str = "Unknown"
    expungement_rules: str = "\\[rules documentation not added yet\\]"

    def __post_init__(self):
        type_eligibility = self._build_type_eligibility()
        self.expungement_result = ExpungementResult(type_eligibility=type_eligibility, time_eligibility=None)

    def _build_type_eligibility(self):
        if self.disposition is None:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not found. Needs further analysis"
            )
        elif self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not recognized. Needs further analysis"
            )
        else:
            return self._default_type_eligibility()

    def _default_type_eligibility(self):
        raise NotImplementedError

    def case(self):
        return self._case

    def acquitted(self):
        # TODO: rename this method and related variables to "dismissed" or similar
        acquittal_statuses = [DispositionStatus.NO_COMPLAINT, DispositionStatus.DISMISSED, DispositionStatus.DIVERTED]
        return self.disposition and self.disposition.status in acquittal_statuses

    def convicted(self):
        return self.disposition and self.disposition.status == DispositionStatus.CONVICTED

    def recent_conviction(self):
        ten_years_ago = date_class.today() + relativedelta(years=-10)
        if self.convicted():
            return self.disposition.date > ten_years_ago  # type: ignore
        else:
            return False

    def recent_acquittal(self):
        three_years_ago = date_class.today() + relativedelta(years=-3)
        return self.acquitted() and self.date > three_years_ago

    def blocks_other_charges(self):
        return True

    def hidden_in_record_summary(self):
        return False

    def set_time_eligibility(self, eligibility_dates):
        date_will_be_eligible, reason = max(eligibility_dates)
        if date_will_be_eligible and date_class.today() >= date_will_be_eligible:
            time_eligibility = TimeEligibility(
                status=EligibilityStatus.ELIGIBLE, reason="", date_will_be_eligible=date_will_be_eligible
            )
        else:
            time_eligibility = TimeEligibility(
                status=EligibilityStatus.INELIGIBLE, reason=reason, date_will_be_eligible=date_will_be_eligible
            )
        self.expungement_result.time_eligibility = time_eligibility
