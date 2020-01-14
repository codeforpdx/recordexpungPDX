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


@dataclass
class TypeEligibility:
    status: EligibilityStatus
    reason: str


@dataclass
class TimeEligibility:
    status: EligibilityStatus
    reason: str
    date_will_be_eligible: Optional[date]


@dataclass
class ChargeEligibility:
    status: ChargeEligibilityStatus
    label: str
    date_will_be_eligible: Optional[date]


@dataclass
class ExpungementResult:
    type_eligibility: TypeEligibility
    time_eligibility: Optional[TimeEligibility]

    def set_type_eligibility(self, type_eligibility):
        self.type_eligibility = type_eligibility

    @property
    def charge_eligibility(self):
        if self.type_eligibility.status == EligibilityStatus.ELIGIBLE:
            if self.time_eligibility and self.time_eligibility.status == EligibilityStatus.ELIGIBLE:
                return ChargeEligibility(ChargeEligibilityStatus.ELIGIBLE_NOW, "Eligible", None)

            elif self.time_eligibility and self.time_eligibility.status == EligibilityStatus.INELIGIBLE:
                if self.time_eligibility.date_will_be_eligible:
                    return ChargeEligibility(
                        ChargeEligibilityStatus.WILL_BE_ELIGIBLE,
                        f"Eligible {self.time_eligibility.date_will_be_eligible.strftime('%b %-d, %Y')}",
                        self.time_eligibility.date_will_be_eligible,
                    )
                else:
                    # Currently, no charge types that are type-eligible can be disqualified due to a time-ineligibility date of None, meaning "never"
                    # So this else block has no applicable cases and never runs. But it will apply if a new charge type that qualifies gets added.
                    return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible", None)
            else:
                return ChargeEligibility(
                    ChargeEligibilityStatus.UNKNOWN, "Type-eligible but time analysis is missing", None
                )

        elif self.type_eligibility.status == EligibilityStatus.NEEDS_MORE_ANALYSIS:
            if self.time_eligibility and self.time_eligibility.status == EligibilityStatus.ELIGIBLE:
                return ChargeEligibility(ChargeEligibilityStatus.POSSIBLY_ELIGIBILE, "Possibly Eligible (review)", None)

            elif self.time_eligibility and self.time_eligibility.status == EligibilityStatus.INELIGIBLE:
                if self.time_eligibility.date_will_be_eligible:
                    return ChargeEligibility(
                        ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                        f"Possibly Eligible {self.time_eligibility.date_will_be_eligible.strftime('%b %-d, %Y')} (review)",
                        self.time_eligibility.date_will_be_eligible,
                    )
                else:
                    # Currently, this occurs with Class B Felonies only, which can be time ineligible with a date of None, meaning "never"
                    return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible", None)
            else:
                return ChargeEligibility(
                    ChargeEligibilityStatus.UNKNOWN, "Possibly eligible but time analysis is missing", None
                )

        elif self.type_eligibility.status == EligibilityStatus.INELIGIBLE:
            return ChargeEligibility(ChargeEligibilityStatus.INELIGIBLE, "Ineligible", None)
