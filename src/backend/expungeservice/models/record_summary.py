from dataclasses import dataclass
from typing import List, Dict, Tuple

from expungeservice.models.record import Record, QuestionSummary


@dataclass
class CaseFine:
    case_number: str
    balance: float


@dataclass
class CountyFines:
    county_name: str
    case_fines: List[CaseFine]

    @property
    def total_fines_due(self):
        return round(sum([case_fines.balance for case_fines in self.case_fines]), 2)


ChargesForSummaryPanel = Tuple[str, List[Tuple[str, List[Tuple[str, str]]]]]


@dataclass
class RecordSummary:
    record: Record
    questions: Dict[str, QuestionSummary]
    total_charges: int
    charges_grouped_by_eligibility_and_case: ChargesForSummaryPanel
    county_fines: List[CountyFines]

    @property
    def total_fines_due(self):
        return round(sum([county_fine.total_fines_due for county_fine in self.county_fines]), 2)

    @property
    def total_cases(self):
        return len(self.record.cases)
