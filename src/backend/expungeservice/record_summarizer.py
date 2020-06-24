from collections import OrderedDict
from itertools import groupby

from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.record import QuestionSummary
from expungeservice.models.record_summary import RecordSummary, CountyBalance
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

        def group(charge: Charge):
            return charge.expungement_result.charge_eligibility.label  # type: ignore

        SHOW_ALL_CHARGES_THRESHOLD = 20
        if len(record.charges) <= SHOW_ALL_CHARGES_THRESHOLD:
            visible_charges = record.charges
        else:
            visible_charges = [charge for charge in record.charges if not charge.charge_type.hidden_in_record_summary()]
        eligible_charges_by_date: Dict[str, List[Tuple[str, str]]] = {}
        for label, charges in groupby(sorted(visible_charges, key=group), key=group):
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
