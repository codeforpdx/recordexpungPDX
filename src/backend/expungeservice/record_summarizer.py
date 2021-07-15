from itertools import groupby

from expungeservice.models.case import Case
from expungeservice.models.record import QuestionSummary, Record
from expungeservice.models.record_summary import RecordSummary, CountyFilingFee, CountyFines, CaseFine
from expungeservice.charges_summarizer import ChargesSummarizer
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from typing import Dict, List, Tuple


class RecordSummarizer:
    @staticmethod
    def summarize(record: Record, questions: Dict[str, QuestionSummary]) -> RecordSummary:
        county_fines, county_filing_fees = RecordSummarizer._build_county_balances(record)
        charges_grouped_by_eligibility_and_case = ChargesSummarizer.build_charges_for_summary_panel(record)
        no_fees_reason = RecordSummarizer._build_no_fees_reason(record.charges)
        return RecordSummary(
            record=record,
            questions=questions,
            charges_grouped_by_eligibility_and_case=charges_grouped_by_eligibility_and_case,
            total_charges=len(record.charges),
            county_fines=county_fines,
            county_filing_fees=county_filing_fees,
            no_fees_reason=no_fees_reason,
        )

    @staticmethod
    def _build_county_balances(record: Record) -> Tuple[List[CountyFines], List[CountyFilingFee]]:
        def get_location(case: Case):
            return case.summary.location

        county_fines_list: List[CountyFines] = []
        county_filing_fees: List[CountyFilingFee] = []
        for location, cases_by_county in groupby(sorted(record.cases, key=get_location), key=get_location):
            cases = list(cases_by_county)
            cases_with_fines = filter(lambda case: case.summary.get_balance_due(), cases)
            fines = [CaseFine(case.summary.case_number, case.summary.get_balance_due()) for case in cases_with_fines]
            cases_with_conviction_fees = [
                case
                for case in cases
                if case.has_eligible_conviction() and not case.qualifying_marijuana_conviction_form_applicable()
            ]
            county_fines_list.append(CountyFines(location, fines))
            if len(cases_with_conviction_fees) > 0:
                county_filing_fees.append(CountyFilingFee(location, len(cases_with_conviction_fees)))
        return county_fines_list, county_filing_fees

    @staticmethod
    def _build_no_fees_reason(charges):
        reason = "None"
        if charges:
            nonconvictions_eligible_now = [
                c
                for c in charges
                if c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
                and c.disposition.status != DispositionStatus.CONVICTED
            ]
            if nonconvictions_eligible_now:
                reason = "$0.00 (no eligible convictions)"
        return reason
