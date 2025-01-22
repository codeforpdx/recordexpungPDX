from dataclasses import dataclass
from expungeservice.util import DateWithFuture as date
from enum import Enum
from typing import Optional


class EligibilityStatus(str, Enum):
    ELIGIBLE = "Eligible"
    NEEDS_MORE_ANALYSIS = "Needs More Analysis"
    INELIGIBLE = "Ineligible"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class ChargeEligibilityStatus(str, Enum):
    UNKNOWN = "Unknown"
    ELIGIBLE_NOW = "Eligible Now"
    POSSIBLY_ELIGIBILE = "Possibly Eligible"
    WILL_BE_ELIGIBLE = "Will Be Eligible"
    POSSIBLY_WILL_BE_ELIGIBLE = "Possibly Will Be Eligible"
    INELIGIBLE = "Ineligible"
    NEEDS_MORE_ANALYSIS = "Needs More Analysis"
    INELIGIBLE_IF_RESTITUTION_OWED = "Ineligible If Restitution Owed"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


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
    date_to_sort_label_by: Optional[date] = None


@dataclass(frozen=True)
class ExpungementResult:
    type_eligibility: TypeEligibility = TypeEligibility(
        status=EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Default value"
    )  # TODO: Remove default value
    time_eligibility: Optional[TimeEligibility] = None
    charge_eligibility: Optional[ChargeEligibility] = None
