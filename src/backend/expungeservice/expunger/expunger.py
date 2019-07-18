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
        self._skipped_charges = []
        self.most_recent_dismissal = None
        self.most_recent_conviction = None
        self.second_most_recent_conviction = None
        self.most_recent_charge = None
        self.num_acquittals = 0
        self.acquittals = []
        self._convictions = []
        self.class_b_felonies = []
        self._time_analyzer = None

    def run(self):
        """
        Evaluates the expungement eligibility of a record.

        :return: True if there are no open cases; otherwise False
        """
        if self._open_cases():
            self.errors.append('Open cases exist')
            return False

        self._tag_skipped_charges()
        self._remove_skipped_charges()
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

    def _tag_skipped_charges(self):
        for charge in self._charges:
            if charge.skip_analysis():
                self._skipped_charges.append(charge)

    def _remove_skipped_charges(self):
        for charge in self._skipped_charges:
            self._charges.remove(charge)

    def _categorize_charges(self):
        for charge in self._charges:
            if charge.acquitted():
                self.acquittals.append(charge)
            else:
                self._convictions.append(charge)

    def _set_most_recent_dismissal(self):
        self.acquittals.sort(key=lambda charge: charge.date)
        if self.acquittals and self.acquittals[-1].recent_acquittal():
            self.most_recent_dismissal = self.acquittals[-1]

    def _set_most_recent_convictions(self):
        self._convictions.sort(key=lambda charge: charge.disposition.date)
        if len(self._convictions) > 0 and self._convictions[-1].recent_conviction():
            self.most_recent_conviction = self._convictions[-1]
        if len(self._convictions) > 1 and self._convictions[-2].recent_conviction():
            self.second_most_recent_conviction = self._convictions[-2]

    def _set_num_acquittals(self):
        for charge in self.acquittals:
            if charge.recent_acquittal():
                self.num_acquittals += 1

    def _assign_most_recent_charge(self):
        self._charges.sort(key=lambda charge: charge.disposition.date, reverse=True)

        if self._charges:
            self.most_recent_charge = self._most_recent_non_traffic_violation()

    def _most_recent_non_traffic_violation(self):
        for charge in self._charges:
            if not charge.motor_vehicle_violation():
                return charge

    def _assign_class_b_felonies(self):
        for charge in self._charges:
            if charge.__class__.__name__ == 'FelonyClassB':
                self.class_b_felonies.append(charge)
