from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class EligibilityStatus(str, Enum):
    ELIGIBLE = "Eligible"
    NEEDS_MORE_ANALYSIS = "Needs more analysis"
    INELIGIBLE = "Ineligible"

@dataclass
class TypeEligibility:
    status: EligibilityStatus
    reason: str

@dataclass
class TimeEligibility:
    status: bool
    reason: str
    date_will_be_eligible: Optional[date]

@dataclass
class ExpungementResult:
    type_eligibility: Optional[TypeEligibility]
    time_eligibility: Optional[TimeEligibility]

    def set_type_eligibility(self, type_eligibility):
        self.type_eligibility = type_eligibility
