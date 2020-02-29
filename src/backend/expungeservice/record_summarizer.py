from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record import Record, Question
from expungeservice.models.record_summary import RecordSummary, CountyBalance
from typing import Dict, List
from datetime import date


class RecordSummarizer:
    @staticmethod
    def summarize(record, questions: List[Question]) -> RecordSummary:
        fully_eligible_cases = []
        fully_ineligible_cases = []
        partially_eligible_cases = []
        other_cases = []

        county_balances: Dict[str, float] = {}
        for case in record.cases:
            if not case.location in county_balances.keys():
                county_balances[case.location] = case.get_balance_due()
            else:
                county_balances[case.location] += case.get_balance_due()

            if all(
                [
                    c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
                    for c in case.charges
                ]
            ):
                fully_eligible_cases.append(case.case_number)
            elif any(
                [
                    c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
                    for c in case.charges
                ]
            ):
                partially_eligible_cases.append(case.case_number)
            elif all(
                [
                    c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
                    and not c.hidden_in_record_summary()
                    for c in case.charges
                ]
            ):
                fully_ineligible_cases.append(case.case_number)
            else:
                other_cases.append(case.case_number)

        cases_sorted = {
            "fully_eligible": fully_eligible_cases,
            "fully_ineligible": fully_ineligible_cases,
            "partially_eligible": partially_eligible_cases,
            "other": other_cases,
        }
        county_balances_list: List[CountyBalance] = []
        for county, balance in county_balances.items():
            county_balances_list.append(CountyBalance(county, round(balance, 2)))
        total_charges = len(record.charges)
        eligible_charges_now = [
            c.name
            for c in record.charges
            if c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
        ]
        eligible_charges_by_date = [["now",eligible_charges_now]]
        will_be_eligible_charges : Dict[date, List[str]] = {}
        for charge in record.charges:
            if charge.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE:
                date_eligible = charge.expungement_result.time_eligibility.date_will_be_eligible
                charge_name = charge.name.split("(")[0]
                if date_eligible not in will_be_eligible_charges.keys():
                    will_be_eligible_charges[date_eligible] = [charge_name]
                else:
                    will_be_eligible_charges[date_eligible].append(charge_name)
        for dateval in sorted(will_be_eligible_charges):
            eligible_charges_by_date.append([dateval.strftime('%b %-d, %Y'), will_be_eligible_charges[dateval]])
        return RecordSummary(
            record=record,
            questions=questions,
            cases_sorted=cases_sorted,
            eligible_charges_by_date=eligible_charges_by_date,
            total_charges=total_charges,
            county_balances=county_balances_list,
        )
