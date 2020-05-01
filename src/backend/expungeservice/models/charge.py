from dataclasses import dataclass, field

from datetime import date as date_class
from typing import Optional

from dateutil.relativedelta import relativedelta

from expungeservice.models.disposition import Disposition, DispositionStatus
from expungeservice.models.expungement_result import (
    ExpungementResult,
    TypeEligibility,
    EligibilityStatus,
)


@dataclass(frozen=True)
class OeciCharge:
    ambiguous_charge_id: str
    name: str
    statute: str
    level: str
    date: date_class
    disposition: Optional[Disposition]
    probation_revoked: Optional[date_class]


@dataclass(frozen=True)
class Charge(OeciCharge):
    id: str
    case_number: str
    expungement_result: ExpungementResult = ExpungementResult()  # TODO: Remove default value
    type_name: str = "Unknown"
    expungement_rules: str = "\\[rules documentation not added yet\\]"

    @property
    def type_eligibility(self) -> TypeEligibility:
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

    def case(self, cases):
        return next(case for case in cases if case.summary.case_number == self.case_number)

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
