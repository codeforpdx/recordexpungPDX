from dataclasses import dataclass, field
from typing import List, Dict, Any

from expungeservice.models.record import Record, Question


@dataclass
class CountyBalance:
    county_name: str
    balance: float


@dataclass
class RecordSummary:
    record: Record
    questions: List[Question]
    total_charges: int
    cases_sorted: Dict[str, List[str]]
    eligible_charges_by_date: List[List[Any]] # Each list element is a list of length 2: [str, List[str]]
    county_balances: List[CountyBalance]

    @property
    def total_balance_due(self):
        return round(sum([county.balance for county in self.county_balances]), 2)

    @property
    def total_cases(self):
        return sum([len(cases) for cases in self.cases_sorted.values()])
