from itertools import groupby

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.record import QuestionSummary, Record
from expungeservice.models.record_summary import RecordSummary, CountyFilingFee, CountyFine
from expungeservice.util import DateWithFuture as date
from typing import Dict, List, Tuple


class RecordSummarizer:
    @staticmethod
    def summarize(record, questions: Dict[str, QuestionSummary]) -> RecordSummary:
        county_fines, county_filing_fees = RecordSummarizer._build_county_balances(record)
        eligible_charges_by_date = RecordSummarizer._build_eligible_charges_by_date(record)
        return RecordSummary(
            record=record,
            questions=questions,
            eligible_charges_by_date=eligible_charges_by_date,
            total_charges=len(record.charges),
            county_fines=county_fines,
            county_filing_fees=county_filing_fees,
        )

    @staticmethod
    def _build_county_balances(record: Record):
        def get_location(case: Case):
            return case.summary.location

        county_fines_list: List[CountyFine] = []
        county_filing_fees: List[CountyFilingFee] = []
        for location, cases_by_county in groupby(sorted(record.cases, key=get_location), key=get_location):
            cases = list(cases_by_county)
            fines = [case.summary.get_balance_due() for case in cases]
            cases_with_eligible_convictions = [case for case in cases if case.has_eligible_conviction()]
            county_fines_list.append(CountyFine(location, round(sum(fines), 2)))
            if len(cases_with_eligible_convictions) > 0:
                county_filing_fees.append(CountyFilingFee(location, len(cases_with_eligible_convictions)))
        return county_fines_list, county_filing_fees

    @staticmethod
    def _build_eligible_charges_by_date(record: Record):
        def primary_sort(charge: Charge):
            charge_eligibility = charge.expungement_result.charge_eligibility
            if charge_eligibility:
                label = charge_eligibility.label
                if label == "Needs More Analysis":
                    return 0, label
                elif label == "Ineligible":
                    return 1, label
                elif label == "Eligible Now":
                    return 2, label
                elif "Eligible Now" in label:
                    return 3, label
                else:
                    return 4, label
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
            visible_charges = [charge for charge in record.charges if not charge.charge_type.hidden_in_record_summary()]
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
