from dataclasses import dataclass
from typing import List, Dict, Tuple

from expungeservice.models.record import Record, QuestionSummary


@dataclass
class CountyBalance:
    county_name: str
    balance: float


@dataclass
class RecordSummary:
    record: Record
    questions: Dict[str, QuestionSummary]
    disposition_was_unknown: List[str]
    total_charges: int
    cases_sorted: Dict[str, List[str]]
    eligible_charges_by_date: List[Tuple[str, List[Tuple[str, str]]]]
    county_balances: List[CountyBalance]

    @property
    def total_balance_due(self):
        return round(sum([county.balance for county in self.county_balances]), 2)

    @property
    def total_cases(self):
        return sum([len(cases) for cases in self.cases_sorted.values()])
