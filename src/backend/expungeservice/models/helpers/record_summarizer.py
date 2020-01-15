from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record_summary import RecordSummary


class RecordSummarizer:
    @staticmethod
    def summarize(record):

        fully_eligible_cases = []
        fully_ineligible_cases = []
        partially_eligible_cases = []
        other_cases = []

        county_balances = {}
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
        for county in county_balances.keys():
            county_balances[county] = round(county_balances[county], 2)
        total_charges = len(record.charges)
        eligible_charges = [
            c.name
            for c in record.charges
            if c.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
        ]
        return RecordSummary(
            cases_sorted=cases_sorted,
            eligible_charges=eligible_charges,
            total_charges=total_charges,
            county_balances=county_balances,
        )
