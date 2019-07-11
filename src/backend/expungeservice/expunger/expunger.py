from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer


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
        '''
        Constructor

        :param record: A Record object
        '''
        self.record = record
        self._charges = record.charges
        self.errors = []
        self._dispositionless_charges = []
        self._most_recent_dismissal = None
        self._most_recent_conviction = None
        self._second_most_recent_conviction = None
        self._most_recent_charge = None
        self._num_acquittals = 0
        self._acquittals = []
        self._convictions = []
        self._class_b_felonies = []
        self._time_analyzer = None

    def run(self):
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        if self._open_cases():
            self.errors.append('Open cases exist')
            return False

        self._tag_dispositionless_charges()
        self._remove_dispositionless_charge()
        self._categorize_charges()
        self._set_most_recent_dismissal()
        self._set_most_recent_convictions()
        self._set_num_acquittals()
        self._assign_most_recent_charge()
        self._assign_class_b_felonies()
        self._time_analyzer = TimeAnalyzer(most_recent_conviction=self._most_recent_conviction,
                                           second_most_recent_conviction=self._second_most_recent_conviction,
                                           most_recent_dismissal=self._most_recent_dismissal,
                                           num_acquittals=self._num_acquittals,
                                           class_b_felonies=self._class_b_felonies,
                                           most_recent_charge=self._most_recent_charge)
        self._time_analyzer.evaluate(self._charges)
        return True

    def _open_cases(self):
        for case in self.record.cases:
            if not case.closed():
                return True
        return False

    def _tag_dispositionless_charges(self):
        for charge in self._charges:
            if Expunger._charge_without_disposition(charge):
                charge.expungement_result.type_eligibility_reason = "Disposition not found. Needs further analysis"
                self._dispositionless_charges.append(charge)

    def _remove_dispositionless_charge(self):
        for charge in self._dispositionless_charges:
            self._charges.remove(charge)

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

    def _set_num_acquittals(self):
        for charge in self._acquittals:
            if charge.recent_acquittal():
                self._num_acquittals += 1

    def _assign_most_recent_charge(self):
        self._charges.sort(key=lambda charge: charge.disposition.date, reverse=True)

        if self._charges:
            self._most_recent_charge = self._most_recent_non_traffic_violation()

    def _most_recent_non_traffic_violation(self):
        for charge in self._charges:
            if not charge.motor_vehicle_violation():
                return charge

    def _assign_class_b_felonies(self):
        for charge in self._charges:
            if charge.__class__.__name__ == 'FelonyClassB':
                self._class_b_felonies.append(charge)

    @staticmethod
    def _charge_without_disposition(charge):
        if not charge.disposition.ruling:
            return True
        else:
            return False
