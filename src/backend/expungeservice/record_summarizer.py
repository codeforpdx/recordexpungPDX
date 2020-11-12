from itertools import groupby

from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.record import QuestionSummary
from expungeservice.models.record_summary import RecordSummary, CountyBalance
from expungeservice.util import DateWithFuture as date
from typing import Dict, List, Tuple


class RecordSummarizer:
    @staticmethod
    def summarize(record, questions: Dict[str, QuestionSummary]) -> RecordSummary:
        county_balances: Dict[str, float] = {}
        for case in record.cases:
            if not case.summary.location in county_balances.keys():
                county_balances[case.summary.location] = case.summary.get_balance_due()
            else:
                county_balances[case.summary.location] += case.summary.get_balance_due()
        county_balances_list: List[CountyBalance] = []
        for county, balance in county_balances.items():
            county_balances_list.append(CountyBalance(county, round(balance, 2)))
        total_charges = len(record.charges)

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

        return RecordSummary(
            record=record,
            questions=questions,
            eligible_charges_by_date=eligible_charges_by_date,
            total_charges=total_charges,
            county_balances=county_balances_list,
        )
