from dataclasses import dataclass
from typing import List, Dict, Tuple

from expungeservice.models.record import Record, QuestionSummary


@dataclass
class CountyBalance:
    county_name: str
    balance: float


@dataclass
class FilingFees:
    cases_with_eligible_convictions: int
    counties_with_eligible_convictions: int

    @property
    def total(self):
        return 281 * self.cases_with_eligible_convictions + 80 * self.counties_with_eligible_convictions


@dataclass
class RecordSummary:
    record: Record
    questions: Dict[str, QuestionSummary]
    total_charges: int
    eligible_charges_by_date: Dict[str, List[Tuple[str, str]]]
    county_balances: List[CountyBalance]

    @property
    def total_balance_due(self):
        return round(sum([county.balance for county in self.county_balances]), 2)

    @property
    def total_cases(self):
        return len(self.record.cases)

    @property
    def filing_fee(self):
        cases_with_eligible_convictions = [case for case in self.record.cases if case.has_eligible_conviction()]
        locations = set([case.summary.location for case in cases_with_eligible_convictions])
        return FilingFees(cases_with_eligible_convictions=len(cases_with_eligible_convictions), counties_with_eligible_convictions=len(locations))
