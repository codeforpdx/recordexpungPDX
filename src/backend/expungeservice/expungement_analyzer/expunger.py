from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expungement_analyzer.analyzers.type_analyzer import TypeAnalyzer


class Expunger:
    """
    This is more or less a wrapper for the time_analyzer and type_analyzer.
    After running this method the results can be extracted from the cases
    attribute. The errors attribute will list the reasons why the run
    method failed to evaluate in which case the run method will return
    False; otherwise there were no errors and it returns True.

    Most of the algorithms in this class can be replaced with database
    query's if/when we start persisting the model objects to the db.
    """

    def __init__(self, cases):
        '''
        Constructor

        :param cases: A list of cases
        '''
        self.cases = cases
        self.errors = []
        self._charges = []
        self._most_recent_dismissal = None
        self._most_recent_conviction = None
        self._second_most_recent_conviction = None
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
        self._set_most_recent_dismissal()
        self._set_most_recent_convictions()
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
            if charge.acquitted():
                self._acquittals.append(charge)
            else:
                self._convictions.append(charge)

    def _set_most_recent_dismissal(self):
        self._acquittals.sort(key=lambda charge: charge.date)
        if self._acquittals and self._acquittals[-1].recent_acquittal():
            self._most_recent_dismissal = self._acquittals[-1]

    def _set_most_recent_convictions(self):
        self._convictions.sort(key=lambda charge: charge.disposition.date)
        if len(self._convictions) > 0 and self._convictions[-1].recent_conviction():
            self._most_recent_conviction = self._convictions[-1]
        if len(self._convictions) > 1 and self._convictions[-2].recent_conviction():
            self._second_most_recent_conviction = self._convictions[-2]
