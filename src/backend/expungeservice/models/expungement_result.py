from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class EligibilityStatus(str, Enum):
    ELIGIBLE = "Eligible"
    NEEDS_MORE_ANALYSIS = "Needs more analysis"
    INELIGIBLE = "Ineligible"


class ChargeEligibilityStatus(str, Enum):
    UNKNOWN = "Unknown"
    ELIGIBLE_NOW = "Eligible now"
    POSSIBLY_ELIGIBILE = "Possibly eligible"
    WILL_BE_ELIGIBLE = "Will be eligible"
    POSSIBLY_WILL_BE_ELIGIBLE = "Possibly will be eligible"
    INELIGIBLE = "Ineligible"


@dataclass(frozen=True)
class TypeEligibility:
    status: EligibilityStatus
    reason: str


@dataclass(frozen=True)
class TimeEligibility:
    status: EligibilityStatus
    reason: str
    date_will_be_eligible: date
    unique_date: bool = True


@dataclass(frozen=True)
class ChargeEligibility:
    status: ChargeEligibilityStatus
    label: str


@dataclass(frozen=True)
class ExpungementResult:
    type_eligibility: TypeEligibility = TypeEligibility(
        status=EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Default value"
    )  # TODO: Remove default value
    time_eligibility: Optional[TimeEligibility] = None
    charge_eligibility: Optional[ChargeEligibility] = None
