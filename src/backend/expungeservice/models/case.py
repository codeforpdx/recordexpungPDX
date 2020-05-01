from dataclasses import dataclass
from datetime import datetime, date as date_class
from typing import Optional, Tuple, Any

from expungeservice.models.charge import OeciCharge, Charge


@dataclass(frozen=True)
class CaseSummary:
    name: str
    birth_year: Optional[int]
    case_number: str
    citation_number: str
    location: str
    date: date_class
    violation_type: str
    current_status: str
    case_detail_link: str
    balance_due_in_cents: int = 0

    def get_balance_due(self):
        return self.balance_due_in_cents / 100

    def closed(self):
        if self._ignore_open_case():
            return True
        else:
            return self._closed()

    @staticmethod
    def _parse_birth_year(info) -> Optional[int]:
        if len(info) > 1:
            return int(info[1].split("/")[-1])
        else:
            return None

    def _ignore_open_case(self):
        return "violation" in self.violation_type.lower() or "municipal parking" == self.violation_type.lower()

    def _closed(self):
        CLOSED_STATUS = ["Closed", "Inactive", "Purgable", "Bankruptcy Pending"]
        return self.current_status in CLOSED_STATUS


@dataclass(frozen=True)
class OeciCase:
    summary: CaseSummary
    charges: Tuple[OeciCharge, ...]


@dataclass(frozen=True)
class Case(OeciCase):
    summary: CaseSummary
    charges: Tuple[Charge, ...]


class CaseCreator:
    @staticmethod
    def create(
        info, case_number, citation_number, date_location, type_status, case_detail_link, balance="0"
    ) -> CaseSummary:
        name = info[0]
        birth_year = CaseSummary._parse_birth_year(info)
        citation_number = citation_number[0] if citation_number else ""
        date, location = date_location
        date = datetime.date(datetime.strptime(date, "%m/%d/%Y"))
        violation_type, current_status = type_status
        balance_due_in_cents = CaseCreator.compute_balance_due_in_cents(balance)
        return CaseSummary(
            name,
            birth_year,
            case_number,
            citation_number,
            location,
            date,
            violation_type,
            current_status,
            case_detail_link,
            balance_due_in_cents,
        )

    @staticmethod
    def compute_balance_due_in_cents(balance_due_dollar_amount: str):
        balance_due_dollar_amount_float = float(balance_due_dollar_amount.replace(",", ""))
        return int(balance_due_dollar_amount_float * 100)
