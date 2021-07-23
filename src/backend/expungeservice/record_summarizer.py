from itertools import groupby

from expungeservice.models.case import Case
from expungeservice.models.record import QuestionSummary, Record
from expungeservice.models.record_summary import RecordSummary, CountyFines, CaseFine
from expungeservice.charges_summarizer import ChargesSummarizer
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from typing import Dict, List, Tuple


class RecordSummarizer:
    @staticmethod
    def summarize(record: Record, questions: Dict[str, QuestionSummary]) -> RecordSummary:
        county_fines = RecordSummarizer._build_county_balances(record)
        charges_grouped_by_eligibility_and_case = ChargesSummarizer.build_charges_for_summary_panel(record)
        return RecordSummary(
            record=record,
            questions=questions,
            charges_grouped_by_eligibility_and_case=charges_grouped_by_eligibility_and_case,
            total_charges=len(record.charges),
            county_fines=county_fines,
        )

    @staticmethod
    def _build_county_balances(record: Record) -> List[CountyFines]:
        def get_location(case: Case):
            return case.summary.location

        county_fines_list: List[CountyFines] = []
        for location, cases_by_county in groupby(sorted(record.cases, key=get_location), key=get_location):
            cases = list(cases_by_county)
            cases_with_fines = filter(lambda case: case.summary.get_balance_due(), cases)
            fines = [CaseFine(case.summary.case_number, case.summary.get_balance_due()) for case in cases_with_fines]
            county_fines_list.append(CountyFines(location, fines))
        return county_fines_list

