from expungeservice.analyzer.ineligible_crimes_list import *

import datetime

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
        self.time_eligible = False

        self.analysis = analysis

        #parse date into proper datetime object
        month, day, year = map(int, self.charge_date.split("/"))
        self.charge_date = datetime.date(year, month, day)


    @property
    def type_elig_result(self):
        return self._result

    @type_elig_result.setter
    def type_elig_result(self, result):
        self._result = result



    #todo: add a method which checks this charge's statute against list A and List B
    #todo: add expungable now t/f










# class Charge(object):
#     """ Charge filed on a Client.
#
#     Attributes:
#         name: A string describing the charge.
#         statute: A Statute object that applies for the charge.
#         date: A datetime.date object specifying the date of the charge.
#         disposition: A Disposition object for the charge.
#     """
#     def __init__(
#             self,
#             name,
#             statute,
#             level,
#             date,
#             disposition):
#         self.name = name
#         self.statute = statute
#         self.level = level
#         self.date = date
#         self.disposition = disposition
#         self._result = None
#
#     @property
#     def type_elig_result(self):
#         return self._result
#
#     @type_elig_result.setter
#     def type_elig_result(self, result):
#         self._result = result