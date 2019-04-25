from datetime import datetime

from expungeservice.expungement_analyzer.type_analyzer import TypeAnalyzer


class Expunger:

    def __init__(self, cases):
        self.cases = cases
        self.errors = []
        self._charges = []
        self._most_recent_acquittal = None
        self._most_recent_conviction = None

    def run(self):
        if self._open_cases():
            self.errors.append('Open cases exist')
            return False

        self._create_charge_list()
        self._set_most_recent_acquittal()
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

    def _set_most_recent_acquittal(self):
        most_recent_acquittal_date = datetime.date(datetime.strptime('01/1/0001', '%m/%d/%Y'))
        for charge in self._charges:
            if charge.disposition.ruling != 'Convicted' and charge.date > most_recent_acquittal_date:
                most_recent_acquittal_date = charge.date
                self._most_recent_acquittal = charge
