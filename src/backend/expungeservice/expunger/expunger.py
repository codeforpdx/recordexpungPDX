from typing import Set, List, Iterator

from more_itertools import flatten

from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from expungeservice.expunger.charges_summarizer import ChargesSummarizer
from expungeservice.models.charge import Charge
from expungeservice.models.disposition import DispositionStatus
from expungeservice.models.record import Record


class Expunger:
    """
    The TimeAnalyzer is probably the last major chunk of non-functional code.
    We mutate the charges in the record directly to add time eligibility information.
    Hence, for example, it is unsafe to deepcopy any elements in the "chain" stemming from record
    including closed_charges, charges, self.charges_with_summary.
    """

    def __init__(self, record: Record):
        self.record = record
        self.all_closed, closed_charges = Expunger._get_closed_charges(self.record)
        charges = Expunger._without_skippable_charges(closed_charges)
        self.charges_with_summary = ChargesSummarizer.summarize(charges)

    def run(self) -> bool:
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        if not self.all_closed:
            self.record.errors += ["All charges are ineligible because there is one or more open case."]
        self.record.errors += self._build_disposition_errors(self.record.charges)
        TimeAnalyzer.evaluate(self.charges_with_summary)
        return self.all_closed

    @staticmethod
    def _get_closed_charges(record: Record):
        closed_cases = [case for case in record.cases if case.closed()]
        closed_charges = flatten([case.charges for case in closed_cases])
        if len(record.cases) == len(closed_cases):
            return True, closed_charges
        else:
            return False, closed_charges

    @staticmethod
    def _without_skippable_charges(charges: Iterator[Charge]):
        return [charge for charge in charges if not charge.skip_analysis() and charge.disposition]

    @staticmethod
    def _build_disposition_errors(charges: List[Charge]):
        record_errors = []
        cases_with_missing_disposition, cases_with_unknown_disposition = Expunger._filter_cases_with_errors(charges)
        if cases_with_missing_disposition:
            record_errors.append(Expunger._build_disposition_error_message(cases_with_missing_disposition, "a missing"))
        if cases_with_unknown_disposition:
            record_errors.append(
                Expunger._build_disposition_error_message(cases_with_unknown_disposition, "an unrecognized")
            )
        return record_errors

    @staticmethod
    def _filter_cases_with_errors(charges: List[Charge]):
        cases_with_missing_disposition: Set[str] = set()
        cases_with_unknown_disposition: Set[str] = set()
        for charge in charges:
            if not charge.skip_analysis():
                case_number = charge.case()().case_number
                if not charge.disposition:
                    cases_with_missing_disposition.add(case_number)
                elif charge.disposition.status == DispositionStatus.UNKNOWN:
                    cases_with_unknown_disposition.add(case_number)
        return cases_with_missing_disposition, cases_with_unknown_disposition

    @staticmethod
    def _build_disposition_error_message(error_cases: Set[str], disposition_error_name: str):
        if len(error_cases) == 1:
            error_message = f"""Case {error_cases.pop()} has a charge with {disposition_error_name} disposition.
This is likely an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges."""
        else:
            cases_list_string = ", ".join(error_cases)
            error_message = f"""The following cases have charges with {disposition_error_name} disposition.
This is likely an error in the OECI database. Time analysis is ignoring these charges and may be inaccurate for other charges.
Case numbers: {cases_list_string}"""
        return error_message
