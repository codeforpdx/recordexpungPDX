from more_itertools import padnone, take

from expungeservice.expunger.analyzers.time_analyzer import TimeAnalyzer
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


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
        self.charges = record.charges
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
            self.record.errors.append('All charges are ineligible because there is one or more open case.')
            return False

        self.charges = Expunger._without_skippable_charges(self.charges)
        self.acquittals, self.convictions, _ = Expunger._categorize_charges(self.charges)
        recent_convictions = Expunger._get_recent_convictions(self.convictions)
        self.most_recent_dismissal = Expunger._most_recent_dismissal(self.acquittals)
        self.most_recent_conviction, self.second_most_recent_conviction = Expunger._most_recent_convictions(recent_convictions)
        self.most_recent_charge = Expunger._most_recent_charge(self.charges)
        self.class_b_felonies = Expunger._class_b_felonies(self.charges)
        TimeAnalyzer.evaluate(self)
        return True

    def _open_cases(self):
        for case in self.record.cases:
            if not case.closed():
                return True
        return False


    @staticmethod
    def _without_skippable_charges(charges):
        return [charge for charge in charges if not charge.skip_analysis() and charge.disposition]

    @staticmethod
    def _categorize_charges(charges):
        acquittals, convictions, unknown = [], [], []
        for charge in charges:
            if charge.acquitted():
                acquittals.append(charge)
            elif charge.convicted():
                convictions.append(charge)
            else:
                unknown.append(charge)
        return acquittals, convictions, unknown

    @staticmethod
    def _get_recent_convictions(convictions):
        recent_convictions = []
        for charge in convictions:
            if charge.recent_conviction():
                recent_convictions.append(charge)
        return recent_convictions

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