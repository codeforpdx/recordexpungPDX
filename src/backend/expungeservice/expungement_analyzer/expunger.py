from datetime import datetime

from expungeservice.expungement_analyzer.type_analyzer import TypeAnalyzer


class Expunger:
    """
    This is a wrapper for the time_analyzer and type_analyzer.
    After running this method the results can be extracted from the
    cases attribute. The errors attribute will list the reason why
    the method returns false (currently there is only one reason).

    Most of the algorithms in this class can be replaced with database
    query's if/when we start persisting the model objects to the db.
    """

    def __init__(self, cases):
        self.cases = cases
        self.errors = []
        self._charges = []
        self._most_recent_acquittal = None
        self._most_recent_conviction = None
        self._acquittals = []
        self._convictions = []

    def run(self):
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        if self._open_cases():
            self.errors.append('Open cases exist')
            return False

        self._create_charge_list()
        self._categorize_charges()
        TypeAnalyzer.evaluate(self._charges)
        return True

    def _open_cases(self):
        for case in self.cases:
            if case.current_status != 'Closed':
                return True
        return False

    def _create_charge_list(self):
        for case in self.cases:
            self._charges.extend(case.charges)

    def _categorize_charges(self):
        for charge in self._charges:
            if TypeAnalyzer.acquitted(charge):
                self._acquittals.append(charge)
            else:
                self._convictions.append(charge)
