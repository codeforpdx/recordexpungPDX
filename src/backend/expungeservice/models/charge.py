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
        type_eligibility = self._type_eligibility()
        if type_eligibility:
            return type_eligibility
        else:
            return self._default_type_eligibility()

    def _default_type_eligibility(self):
        if self.disposition is None:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not found. Needs further analysis"
            )
        elif self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not recognized. Needs further analysis"
            )
        else:
            # This block should never run, because we assume the charge disposition is always convicted, dismissed, unrecognized, or missing.
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Type eligibility could not be determined"
            )

    def _type_eligibility(self):
        """If the disposition is present and recognized, this should always return a TypeEligibility.
It may also return the eligibility without a known disposition (this works for some types).
If the type eligibility is unknown, the method can return None. """
        raise NotImplementedError

    def case(self):
        return self._case

    def dismissed(self):
        dismissal_status = [DispositionStatus.NO_COMPLAINT, DispositionStatus.DISMISSED, DispositionStatus.DIVERTED]
        return self.disposition and self.disposition.status in dismissal_status

    def convicted(self):
        return self.disposition and self.disposition.status == DispositionStatus.CONVICTED

    def recent_conviction(self):
        ten_years_ago = date_class.today() + relativedelta(years=-10)
        if self.convicted():
            return self.disposition.date > ten_years_ago  # type: ignore
        else:
            return False

    def recent_dismissal(self):
        three_years_ago = date_class.today() + relativedelta(years=-3)
        return self.dismissed() and self.date > three_years_ago

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
