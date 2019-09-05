from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from datetime import date as date_class
from dateutil.relativedelta import relativedelta


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
        most_recent_conviction: Most recent conviction if one exists from within the last ten years
        second_most_recent_conviction: Second most recent conviction if one exists from within the last ten years
        most_recent_dismissal: Most recent dismissal if one exists from within the last three years
        num_acquittals: Number of acquittals within the last three years
        class_b_felonies: A list of class B felonies; excluding person crimes or firearm crimes
        most_recent_charge: The most recent charge within the last 20yrs; excluding traffic violations

        :param record: A Record object
        '''
        self.record = record
        self.charges = record.charges
        self.errors = []
        self._skipped_charges = []
        self.most_recent_dismissal = None
        self.most_recent_conviction = None
        self.second_most_recent_conviction = None
        self.most_recent_charge = None
        self.acquittals = []
        self.convictions = []
        self.class_b_felonies = []

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
        self._assign_most_recent_charge()
        self._assign_class_b_felonies()
        TimeAnalyzer.evaluate(self)
        return True

    def _open_cases(self):
        for case in self.record.cases:
            if not case.closed():
                return True
        return False

    def _tag_skipped_charges(self):
        for charge in self.charges:
            if Expunger._dispositionless(charge) or charge.skip_analysis():
                self._skipped_charges.append(charge)

    @staticmethod
    def _dispositionless(charge):
        if charge.disposition is None:
            charge.expungement_result.type_eligibility_reason = "Disposition not found. Needs further analysis"
            return True

    def _remove_skipped_charges(self):
        for charge in self._skipped_charges:
            self.charges.remove(charge)

    def _categorize_charges(self):
        for charge in self.charges:
            if charge.acquitted():
                self.acquittals.append(charge)
            else:
                self.convictions.append(charge)

    def _set_most_recent_dismissal(self):
        self.acquittals.sort(key=lambda charge: charge.date)
        if self.acquittals and self.acquittals[-1].recent_acquittal():
            self.most_recent_dismissal = self.acquittals[-1]

    def _set_most_recent_convictions(self):
        self.convictions.sort(key=lambda charge: charge.disposition.date)
        if len(self.convictions) > 0 and self.convictions[-1].recent_conviction():
            self.most_recent_conviction = self.convictions[-1]
        if len(self.convictions) > 1 and self.convictions[-2].recent_conviction():
            self.second_most_recent_conviction = self.convictions[-2]

    def _assign_most_recent_charge(self):
        self.charges.sort(key=lambda charge: charge.disposition.date, reverse=True)
        if self.charges:
            self.most_recent_charge = self.charges[0]

    def _assign_class_b_felonies(self):
        for charge in self.charges:
            if charge.__class__.__name__ == 'FelonyClassB':
                self.class_b_felonies.append(charge)
