from dataclasses import dataclass
from typing import List, Dict, Tuple

from expungeservice.models.record import Record, QuestionSummary


@dataclass
class CountyFine:
    county_name: str
    balance: float


@dataclass
class CountyFilingFee:
    county_name: str
    cases_with_eligible_convictions: int


@dataclass
class RecordSummary:
    record: Record
    questions: Dict[str, QuestionSummary]
    total_charges: int
    eligible_charges_by_date: Dict[str, List[Tuple[str, str]]]
    county_fines: List[CountyFine]
    county_filing_fees: List[CountyFilingFee]

    @property
    def total_balance_due(self):
        return round(sum([county.balance for county in self.county_fines]), 2)

    @property
    def total_filing_fees_due(self):
        total = 0
        for county in self.county_filing_fees:
            fee_per_case = county.cases_with_eligible_convictions * 281
            fingerprint_fee = 80
            total += fee_per_case + fingerprint_fee
        return total

    @property
    def total_cases(self):
        return len(self.record.cases)
