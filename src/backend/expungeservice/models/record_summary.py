from dataclasses import dataclass, field
from typing import List, Dict

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge


@dataclass
class RecordSummary:
    total_charges: int
    cases_sorted: Dict[str, List[str]]
    eligible_charges: List[str]
    county_balances: Dict[str, float]

    @property
    def total_balance_due(self):
        return sum(self.county_balances.values())

    @property
    def total_cases(self):
        return sum([len(cases) for cases in self.cases_sorted.values()])
