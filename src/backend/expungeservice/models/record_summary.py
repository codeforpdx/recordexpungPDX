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
        total_in_cents = 0
        for county in self.county_balances.keys():
            total_in_cents += round(self.county_balances[county] * 100)
        return round(total_in_cents / 100.0, 2)

    @property
    def total_cases(self):
        return sum([len(self.cases_sorted[key]) for key in self.cases_sorted.keys()])
