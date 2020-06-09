from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record import QuestionSummary
from expungeservice.models.record_summary import RecordSummary, CountyBalance
from typing import Dict, List, Tuple
from expungeservice.util import DateWithFuture as date


class RecordSummarizer:
    @staticmethod
    def filter_charge_names_by_eligibility(charges, eligibility):
        return [
            (c.ambiguous_charge_id, c.to_one_line())
            for c in charges
            if (
                c.expungement_result.charge_eligibility.status == eligibility
                and not c.charge_type.hidden_in_record_summary()
            )
        ]

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
        eligible_charges_now = RecordSummarizer.filter_charge_names_by_eligibility(
            record.charges, ChargeEligibilityStatus.ELIGIBLE_NOW
        )
        eligible_charges_by_date: List[Tuple[str, List[Tuple[str, str]]]] = [("Eligible now", eligible_charges_now)]
        will_be_eligible_charges: Dict[date, List[Tuple[str, str]]] = {}
        needs_more_analysis_charges: List[Tuple[str, str]] = []  # TODO: This list may be incomplete
        for charge in record.charges:
            charge_string = charge.to_one_line()
            if charge.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE:
                if charge.expungement_result.time_eligibility.unique_date:
                    date_eligible = charge.expungement_result.time_eligibility.date_will_be_eligible
                    if will_be_eligible_charges.get(date_eligible):
                        will_be_eligible_charges[date_eligible].append((charge.ambiguous_charge_id, charge_string))
                    else:
                        will_be_eligible_charges[date_eligible] = [(charge.ambiguous_charge_id, charge_string)]
                else:
                    needs_more_analysis_charges.append((charge.ambiguous_charge_id, charge_string))
            elif charge.expungement_result.charge_eligibility.status in [
                ChargeEligibilityStatus.POSSIBLY_ELIGIBILE,
                ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE,
                ChargeEligibilityStatus.UNKNOWN,
            ]:
                needs_more_analysis_charges.append((charge.ambiguous_charge_id, charge_string))
        for date_value in sorted(will_be_eligible_charges):
            eligible_charges_by_date.append(
                ("Eligible " + date_value.strftime("%b %-d, %Y"), will_be_eligible_charges[date_value])
            )
        ineligible_charges = RecordSummarizer.filter_charge_names_by_eligibility(
            record.charges, ChargeEligibilityStatus.INELIGIBLE
        )
        eligible_charges_by_date.append(("Ineligible", ineligible_charges))
        eligible_charges_by_date.append(("Need more analysis", needs_more_analysis_charges))

        return RecordSummary(
            record=record,
            questions=questions,
            eligible_charges_by_date=eligible_charges_by_date,
            total_charges=total_charges,
            county_balances=county_balances_list,
        )
