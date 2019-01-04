import datetime
from expungeservice.expunger.helper_functions import *


class Charge(object):
    """ Charge filed on a Client.

    Attributes:
        name: A string describing the charge.
        statute: A Statute object that applies for the charge.
        date: A datetime.date object specifying the date of the charge.
        disposition: A Disposition object for the charge.
    """
    def __init__(
            self,
            name,
            statute = None, #this comes from the detail page
            level = None,
            charge_date = None,
            disposition = None,
            analysis=None):

        self.name = name
        self.statute = statute
        self.level = level
        self.charge_date = charge_date
        self.disposition = disposition
        self._result = None

        self.type_eligible = False  # this is going to be a bool that represents if this is expungable
        self.type_eligible_analysis = ''
        self.time_eligible = False
        self.time_eligible_analysis = ''

        self.eligible_now = ''
        self.eligible_when = ''

        self.analysis = analysis

        # parse date into proper datetime object, if it is a string #todo: remove this
        if type(self.charge_date) == type(""):
            self.charge_date = date2obj(self.charge_date)



    @property
    def time_elig_result(self):
        return self.time_eligible

    @time_elig_result.setter
    def time_elig_result(self, result):
        self.time_eligible = result

    @property
    def type_elig_result(self):
        return self._result

    @type_elig_result.setter
    def type_elig_result(self, result):
        self._result = result

    def __eq__(self, other):
        return (self.name == other.name and
                self.statute == other.statute and
                self.level == other.level and
                self.charge_date == other.charge_date and
                self.disposition == other.disposition)



    #todo: add a method which checks this charge's statute against list A and List B
    #todo: add expungable now t/f
