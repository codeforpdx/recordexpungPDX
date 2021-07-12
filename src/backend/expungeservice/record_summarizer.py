from itertools import groupby

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.record import QuestionSummary, Record
from expungeservice.models.record_summary import RecordSummary, CountyFilingFee, CountyFines, CaseFine
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.util import DateWithFuture as date
from typing import Dict, List, Tuple


class RecordSummarizer:
    @staticmethod
    def summarize(record, questions: Dict[str, QuestionSummary]) -> RecordSummary:
        county_fines, county_filing_fees = RecordSummarizer._build_county_balances(record)
        eligible_charges_by_date = RecordSummarizer._build_eligible_charges_by_date(record)
        charges_grouped_by_eligibility_and_case = RecordSummarizer._build_charges_grouped_by_eligibility_and_case(record)
        no_fees_reason = RecordSummarizer._build_no_fees_reason(record.charges)
        return RecordSummary(
            record=record,
            questions=questions,
            eligible_charges_by_date=eligible_charges_by_date,

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
    def _build_eligible_charges_by_date(record: Record):
        def primary_sort(charge: Charge):
            charge_eligibility = charge.expungement_result.charge_eligibility
            if charge_eligibility:
                label = charge_eligibility.label
                no_balance = RecordSummarizer._get_case_of_charge(record, charge).summary.balance_due_in_cents == 0
                if label == "Needs More Analysis":
                    return 0, label
                elif label == "Ineligible":
                    return 1, label
                elif label == "Eligible Now":
                    if no_balance:
                        return 2, label
                    else:
                        return 3, label + " If Balance Paid"
                elif "Eligible Now" in label: #I don't know what this is for -J
                    if no_balance:
                        return 4, label
                    else:
                        return 5, label + " If Balance Paid"
                else:
                    if no_balance:
                        return 6, label
                    else:
                        return 7, label + " If Balance Paid"
            else:
                return 0, ""

        def secondary_sort(charge: Charge):
            charge_eligibility = charge.expungement_result.charge_eligibility
            if charge_eligibility and charge_eligibility.date_to_sort_label_by:
                return charge_eligibility.date_to_sort_label_by
            else:
                return date.max()

        def get_label(charge: Charge):
            charge_eligibility = charge.expungement_result.charge_eligibility
            if charge_eligibility:
                return charge_eligibility.label
            else:
                return ""  # TODO: Rethink if possible

        SHOW_ALL_CHARGES_THRESHOLD = 20
        if len(record.charges) <= SHOW_ALL_CHARGES_THRESHOLD:
            visible_charges = record.charges
        else:
            visible_charges = [charge for charge in record.charges_without_case_balance if not charge.charge_type.hidden_in_record_summary()]
        eligible_charges_by_date: Dict[str, List[Tuple[str, str]]] = {}
        sorted_charges = sorted(sorted(visible_charges, key=secondary_sort, reverse=True), key=primary_sort)
        for label, charges in groupby(sorted_charges, key=get_label):
            charges_tuples = [
                (charge.ambiguous_charge_id, charge.to_one_line())
                for charge in charges
                if charge.edit_status != EditStatus.DELETE
            ]
            eligible_charges_by_date[label] = charges_tuples
        return eligible_charges_by_date

    @staticmethod
    def _build_charges_grouped_by_eligibility_and_case(record: Record):
        charges_grouped_by_eligibility_and_case : Dict[str, List[Tuple[str,List[Tuple[str, str]]]]]= {}
        eligible_charges_by_date = RecordSummarizer._build_eligible_charges_by_date(record)
        # this actually groups by labels. We need to push everything down another layer to group by case
        # the data structure is: structure_charges{label: [list of cases] [case has charges] charge is a name and an extra string of some kind.
        for label, charges_under_eligibility_label in eligible_charges_by_date.items():
            charges_grouped_by_eligibility_and_case[label]: List[Tuple[str,List[Tuple[str, str]]]] = []
            previous_case_number = ""
            for charge, one_line_info in charges_under_eligibility_label:
                case_number = "the-case-number"  # charge.case_number
                if case_number == previous_case_number:
                    charges_grouped_by_eligibility_and_case[label][-1][1].append((charge,one_line_info))
                else:
                    charges_grouped_by_eligibility_and_case[label].append((case_number, [(charge, one_line_info)]))
                    previous_case_number=case_number
        return charges_grouped_by_eligibility_and_case
    @staticmethod
    def _get_case_of_charge(record, charge):
        for case in record.cases:
            if charge.case_number == case.summary.case_number:
                return case

    def _get_case_balance_header_info_for_case(case):
        return f'{case.summary.case_number} {case.summary.location} {case.summary.get_balance_due}'

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
