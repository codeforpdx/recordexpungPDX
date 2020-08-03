from dataclasses import dataclass

from typing import Optional, Any

from dateutil.relativedelta import relativedelta
from enum import Enum

from expungeservice.util import DateWithFuture as date_class
from expungeservice.models.disposition import Disposition, DispositionStatus
from expungeservice.models.expungement_result import (
    ExpungementResult,
    TypeEligibility,
    EligibilityStatus,
)


class EditStatus(str, Enum):
    UNCHANGED = "UNCHANGED"
    UPDATE = "UPDATE"
    ADD = "ADD"
    DELETE = "DELETE"


class ChargeUtil:
    @staticmethod
    def dismissed(disposition):
        dismissal_status = [DispositionStatus.NO_COMPLAINT, DispositionStatus.DISMISSED, DispositionStatus.DIVERTED]
        return disposition.status in dismissal_status

    @staticmethod
    def convicted(disposition):
        return disposition.status == DispositionStatus.CONVICTED


@dataclass(frozen=True)
class OeciCharge:
    ambiguous_charge_id: str
    name: str
    statute: str
    level: str
    date: date_class
    disposition: Disposition
    probation_revoked: Optional[date_class]
    balance_due_in_cents: int
    edit_status: EditStatus


@dataclass(frozen=True)
class ChargeType:
    type_name: str = "Unknown"
    expungement_rules: Any = "Select an answer to view more info about its corresponding charge type."
    blocks_other_charges: bool = True

    def type_eligibility(self, disposition):
        """If the disposition is present and recognized, this should always return a TypeEligibility.
It may also return the eligibility without a known disposition (this works for some types).
If the type eligibility is unknown, the method can return None. """
        raise NotImplementedError

    def hidden_in_record_summary(self):
        return False


@dataclass(frozen=True)
class Charge(OeciCharge):
    id: str
    case_number: str
    charge_type: ChargeType
    expungement_result: ExpungementResult = ExpungementResult()  # TODO: Remove default value

    @property
    def type_eligibility(self) -> TypeEligibility:
        type_eligibility = self.charge_type.type_eligibility(self.disposition)
        if type_eligibility:
            return type_eligibility
        else:
            return self._default_type_eligibility()

    def _default_type_eligibility(self):
        if self.disposition.status == DispositionStatus.UNKNOWN:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not found. Needs further analysis"
            )
        elif self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Disposition not recognized. Needs further analysis"
            )
        else:
            raise ValueError(
                "This block should never run, because we assume the charge disposition is always convicted, dismissed, unrecognized, or missing."
            )

    def case(self, cases):
        return next(case for case in cases if case.summary.case_number == self.case_number)

    def dismissed(self):
        return ChargeUtil.dismissed(self.disposition)

    def convicted(self):
        return ChargeUtil.convicted(self.disposition)

    def recent_conviction(self):
        ten_years_ago = date_class.today() + relativedelta(years=-10)
        if self.convicted():
            return self.disposition.date > ten_years_ago
        else:
            return False

    def recent_dismissal(self):
        three_years_ago = date_class.today() + relativedelta(years=-3)
        return self.dismissed() and self.date > three_years_ago

    def to_one_line(self) -> str:
        short_name = self.name.split("(")[0]
        charged_date = self.date.strftime("%b %-d, %Y")
        disposition = str(self.disposition.status.name)
        owed = f" - $ owed" if self.balance_due_in_cents > 0 else ""
        return f"{short_name} ({disposition}) - Charged {charged_date}{owed}"
