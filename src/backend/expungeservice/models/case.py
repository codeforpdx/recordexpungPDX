from dataclasses import dataclass
from datetime import datetime
from expungeservice.util import DateWithFuture as date_class
from typing import Optional, Tuple
import re

from expungeservice.models.charge import OeciCharge, Charge, EditStatus


@dataclass(frozen=True)
class CaseSummary:
    name: str
    birth_year: Optional[int]
    case_number: str
    district_attorney_number: str
    citation_number: str
    location: str
    date: date_class
    violation_type: str
    current_status: str
    case_detail_link: str
    balance_due_in_cents: int
    edit_status: EditStatus

    def get_balance_due(self):
        return self.balance_due_in_cents / 100

    @staticmethod
    def _parse_birth_year(info) -> Optional[int]:
        if len(info) > 1:
            return int(info[1].split("/")[-1])
        else:
            return None

    def closed(self):
        CLOSED_STATUS = ["Closed", "Inactive", "Purgable", "Bankruptcy Pending"]
        return self.current_status in CLOSED_STATUS


@dataclass(frozen=True)
class OeciCase:
    summary: CaseSummary
    charges: Tuple[OeciCharge, ...]

    @staticmethod
    def empty(case_number: str):
        return OeciCase(
            CaseSummary(
                name="",
                birth_year=1900,
                case_number=case_number,
                district_attorney_number="",
                citation_number="",
                location="",
                date=date_class.today(),
                violation_type="",
                current_status="",
                case_detail_link="",
                balance_due_in_cents=0,
                edit_status=EditStatus.UNCHANGED,
            ),
            (),
        )


@dataclass(frozen=True)
class Case(OeciCase):
    summary: CaseSummary
    charges: Tuple[Charge, ...]


class CaseCreator:
    @staticmethod
    def create(
        info,
        case_number,
        district_attorney_number,
        citation_number,
        date_location,
        type_status,
        case_detail_link,
        balance="0",
    ) -> CaseSummary:
        name = info[0]
        birth_year = CaseSummary._parse_birth_year(info)
        citation_number = citation_number[0] if citation_number else ""
        date, location = date_location
        date = date_class.fromdatetime(datetime.strptime(date, "%m/%d/%Y"))
        violation_type, current_status = type_status
        balance_due_in_cents = CaseCreator.compute_balance_due_in_cents(balance)
        return CaseSummary(
            name,
            birth_year,
            case_number,
            district_attorney_number,
            citation_number,
            location,
            date,
            violation_type,
            current_status,
            case_detail_link,
            balance_due_in_cents,
            EditStatus.UNCHANGED,
        )

    @staticmethod
    def compute_balance_due_in_cents(balance_due_dollar_amount: str):
        return int(CaseCreator._balance_to_float(balance_due_dollar_amount) * 100)

    @staticmethod
    def _balance_to_float(balance: str) -> float:
        commas_removed = balance.replace(",","")
        normalized_negative = re.sub("\((?P<balance>.*)\)", "-\g<balance>", commas_removed)
        return float(normalized_negative)
