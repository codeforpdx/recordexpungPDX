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


@dataclass
class CountyFilingFee:
    county_name: str
    cases_with_eligible_convictions: int

ChargesForSummaryPanel = Dict[str, List[Tuple[str,List[Tuple[str, str]]]]]

@dataclass
class RecordSummary:
    record: Record
    questions: Dict[str, QuestionSummary]
    total_charges: int
    charges_grouped_by_eligibility_and_case: ChargesForSummaryPanel
    county_fines: List[CountyFines]
    county_filing_fees: List[CountyFilingFee]
    no_fees_reason: str

    @property
    def total_fines_due(self):
        return round(sum([county_fine.total_fines_due for county_fine in self.county_fines]), 2)

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
