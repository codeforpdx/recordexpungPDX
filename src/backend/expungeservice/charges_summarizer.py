from itertools import groupby

from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.record import Record
from expungeservice.models.record_summary import ChargesForSummaryPanel
from expungeservice.util import DateWithFuture as date
from typing import Dict, List, Tuple


class ChargesSummarizer:
    @staticmethod
    def build_charges_for_summary_panel(record: Record) -> ChargesForSummaryPanel:
        visible_charges = [
            charge for charge in record.charges if not charge.charge_type.hidden_in_record_summary(charge.disposition)
        ]
        eligible_charges_by_date: Dict[str, List[Tuple[str, List[Tuple[str, str]]]]] = {}
        sorted_charges = sorted(
            sorted(visible_charges, key=ChargesSummarizer._secondary_sort, reverse=True),
            key=lambda charge: ChargesSummarizer._primary_sort(charge, record),
        )
        for label, charges in groupby(sorted_charges, key=lambda charge: ChargesSummarizer._get_label(charge, record)):
            charges_in_section: List[Tuple[str, List[Tuple[str, str]]]] = []
            for case_number, case_charges in groupby(charges, key=lambda charge: charge.case_number):
                case = ChargesSummarizer._get_case_by_case_number(record, case_number)
                case_info_line = ChargesSummarizer._get_case_balance_header_info_for_case(case, label)
                charges_tuples = [
                    (case_charge.ambiguous_charge_id, case_charge.to_one_line())
                    for case_charge in case_charges
                    if case_charge.edit_status != EditStatus.DELETE
                ]
                charges_in_section.append((case_info_line, charges_tuples))
            eligible_charges_by_date[label] = charges_in_section
        return eligible_charges_by_date

    @staticmethod
    def _primary_sort(charge: Charge, record: Record):
        charge_eligibility = charge.expungement_result.charge_eligibility
        if charge_eligibility:
            label = charge_eligibility.label
            no_balance = (
                ChargesSummarizer._get_case_by_case_number(record, charge.case_number).summary.balance_due_in_cents == 0
            )
            if label == "Needs More Analysis":
                return 0, label
            elif label == "Ineligible":
                return 1, label
            elif label == "Eligible Now":
                if no_balance:
                    return 2, label
                else:
                    return 3, label + " If Balance Paid"
            elif "Eligible Now" in label:
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

    @staticmethod
    def _secondary_sort(charge: Charge):
        charge_eligibility = charge.expungement_result.charge_eligibility
        if charge_eligibility and charge_eligibility.date_to_sort_label_by:
            return charge_eligibility.date_to_sort_label_by
        else:
            return date.max()

    @staticmethod
    def _get_label(charge: Charge, record: Record):
        no_balance = (
            ChargesSummarizer._get_case_by_case_number(record, charge.case_number).summary.balance_due_in_cents == 0
        )
        charge_eligibility = charge.expungement_result.charge_eligibility
        if charge_eligibility:
            if (
                charge_eligibility.label == "Needs More Analysis"
                or charge_eligibility.label == "Ineligible"
                or no_balance
            ):
                return charge_eligibility.label
            else:
                return charge_eligibility.label + " If Balance Paid"
        else:
            return ""  # TODO: Add error logging because this should be logged as an error

    @staticmethod
    def _get_case_by_case_number(record, case_number):
        for case in record.cases:
            if case_number == case.summary.case_number:
                return case

    @staticmethod
    def _get_case_balance_header_info_for_case(case, label):
        if case.summary.get_balance_due() == 0 or "If Balance Paid" not in label:
            return ""
        else:
            return f"{case.summary.location} {case.summary.case_number} – ${round(case.summary.get_balance_due(),2)}"
