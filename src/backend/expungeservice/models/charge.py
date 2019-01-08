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

        self.type_eligible = None  # this is going to be a bool that represents if this is expungable
        self.time_eligible = None

        self.eligible_now = None
        self.eligible_when = None
        self.analysis = analysis

        # parse date into proper datetime object, if it is a string #todo: remove this
        if type(self.charge_date) == type(""):
            self.charge_date = date2obj(self.charge_date)

    # def __dict__(self):
    #
    #     if self.type_eligible == None or self.time_eligible == None:
    #         return {'name': self.name,
    #                 'statute': self.statute.__dict__(),
    #                 'level': self.level.__dict__(),
    #                 'charge_date': str(self.charge_date),
    #                 'disposition': self.disposition.__dict__(),
    #                 'type_eligible': self.type_eligible,
    #                 'time_eligible': self.time_eligible,
    #                 'eligible_now': self.eligible_now,
    #                 'eligible_when': str(self.eligible_when),
    #                 'analysis': self.analysis
    #                 }
    #
    #     return {'name': self.name,
    #             'statute': self.statute.__dict__(),
    #             'level': self.level.__dict__(),
    #             'charge_date': str(self.charge_date),
    #             'disposition': self.disposition.__dict__(),
    #             'type_eligible': self.type_eligible.__dict__(),
    #             'time_eligible': self.time_eligible.__dict__(),
    #             'eligible_now': self.eligible_now,
    #             'eligible_when': str(self.eligible_when),
    #             'analysis': self.analysis
    #             }

    def __eq__(self, other):
        return (self.name == other.name and
                self.statute == other.statute and
                self.level == other.level and
                self.charge_date == other.charge_date and
                self.disposition == other.disposition)

    # @property
    # def time_elig_result(self):
    #     return self.time_eligible
    #
    # @time_elig_result.setter
    # def time_elig_result(self, result):
    #     self.time_eligible = result
    #
    # @property
    # def type_elig_result(self):
    #     return self._result
    #
    # @type_elig_result.setter
    # def type_elig_result(self, result):
    #     self._result = result





    #todo: add a method which checks this charge's statute against list A and List B
    #todo: add expungable now t/f
