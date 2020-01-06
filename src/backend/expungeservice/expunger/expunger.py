from typing import Set
from more_itertools import padnone, take, flatten

from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.disposition import DispositionStatus


class Expunger:
    """
    This is more or less a wrapper for the time_analyzer.
    After running this method the results can be extracted from the cases
    attribute. The errors attribute will list the reasons why the run
    method failed to evaluate in which case the run method will return
    False; otherwise there were no errors and it returns True.

    Most of the algorithms in this class can be replaced with database
    query's if/when we start persisting the model objects to the db.
    """

    def __init__(self, record):
        """
        Constructor
        most_recent_conviction: Most recent conviction if one exists from within the last ten years
        second_most_recent_conviction: Second most recent conviction if one exists from within the last ten years
        most_recent_dismissal: Most recent dismissal if one exists from within the last three years
        num_acquittals: Number of acquittals within the last three years
        class_b_felonies: A list of class B felonies; excluding person crimes or firearm crimes
        most_recent_charge: The most recent charge within the last 20yrs; excluding traffic violations

        :param record: A Record object
        """
        self.record = record
        self.all_closed, closed_charges = Expunger.get_closed_charges(self.record)
        self.charges = Expunger._without_skippable_charges(closed_charges)
        self.acquittals, self.convictions, self.unknowns = Expunger._categorize_charges(self.charges)
        recent_convictions, self.old_convictions = Expunger._categorize_convictions_by_recency(self.convictions)
        self.most_recent_dismissal = Expunger._most_recent_dismissal(self.acquittals)
        self.most_recent_conviction, self.second_most_recent_conviction = Expunger._most_recent_convictions(recent_convictions)
        self.most_recent_charge = Expunger._most_recent_charge(self.charges)
        self.class_b_felonies = Expunger._class_b_felonies(self.charges)

    def run(self):
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        if not self.all_closed:
            self.record.errors += ["All charges are ineligible because there is one or more open case."]
        self.record.errors += self._build_disposition_errors(self.record.charges)
        TimeAnalyzer.evaluate(self)
        return self.all_closed

    @staticmethod
    def get_closed_charges(record):
        closed_cases = [case for case in record.cases if case.closed()]
        closed_charges = flatten([case.charges for case in closed_cases])
        if len(record.cases) == len(closed_cases):
            return True, closed_charges
        else:
            return False, closed_charges

    @staticmethod
    def _without_skippable_charges(charges):
        return [charge for charge in charges if not charge.skip_analysis() and charge.disposition]

    @staticmethod
    def _categorize_charges(charges):
        acquittals, convictions, unknowns = [], [], []
        for charge in charges:
            if charge.acquitted():
                acquittals.append(charge)
            elif charge.convicted():
                convictions.append(charge)
            else:
                unknowns.append(charge)
        return acquittals, convictions, unknowns

    @staticmethod
    def _categorize_convictions_by_recency(convictions):
        recent_convictions = []
        old_convictions = []
        for charge in convictions:
            if charge.recent_conviction():
                recent_convictions.append(charge)
            else:
                old_convictions.append(charge)
        return recent_convictions, old_convictions

    @staticmethod
    def _most_recent_dismissal(acquittals):
        acquittals.sort(key=lambda charge: charge.date)
        if acquittals and acquittals[-1].recent_acquittal():
            return acquittals[-1]
        else:
            return None

    @staticmethod
    def _most_recent_convictions(recent_convictions):
        recent_convictions.sort(key=lambda charge: charge.disposition.date, reverse=True)
        first, second, third = take(3, padnone(recent_convictions))
        if first and "violation" in first.level.lower():
            return second, third
        elif second and "violation" in second.level.lower():
            return first, third
        else:
            return first, second

    @staticmethod
    def _most_recent_charge(charges):
        charges.sort(key=lambda charge: charge.disposition.date, reverse=True)
        if charges:
            return charges[0]
        else:
            return None

    @staticmethod
    def _class_b_felonies(charges):
        class_b_felonies = []
        for charge in charges:
            if isinstance(charge, FelonyClassB):
                class_b_felonies.append(charge)
        return class_b_felonies

    @staticmethod
    def _build_disposition_errors(charges):
        record_errors = []
        cases_with_missing_disposition, cases_with_unknown_disposition = Expunger._filter_cases_with_errors(charges)
        if cases_with_missing_disposition:
            record_errors.append(Expunger._build_disposition_error_message(
                cases_with_missing_disposition, "a missing"))
        if cases_with_unknown_disposition:
            record_errors.append(Expunger._build_disposition_error_message(
                cases_with_unknown_disposition, "an unrecognized"))
        return record_errors

    @staticmethod
    def _filter_cases_with_errors(charges):
        cases_with_missing_disposition : Set[str] = set()
        cases_with_unknown_disposition : Set[str] = set()
        for charge in charges:
            if not charge.skip_analysis():
                case_number = charge.case()().case_number
                if not charge.disposition:
                    cases_with_missing_disposition.add(case_number)
                elif charge.disposition.status == DispositionStatus.UNKNOWN:
                    cases_with_unknown_disposition.add(case_number)
        return cases_with_missing_disposition, cases_with_unknown_disposition

    @staticmethod
    def _build_disposition_error_message(error_cases, disposition_error_name):
        if len(error_cases) == 1:
                error_message = (
f"""Case {error_cases.pop()} has a charge with {disposition_error_name} disposition.
This is likely an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges.""")
        else:
            cases_list_string = ", ".join(error_cases)
            error_message = (
f"""The following cases have charges with {disposition_error_name} disposition.
This is likely an error in the OECI database. Time analysis is ignoring these charges and may be inaccurate for other charges.
Case numbers: {cases_list_string}""")
        return error_message
