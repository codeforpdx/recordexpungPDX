from expungeservice.expunger.helper_functions import *

class Client(object):
    """ Client - An individual who wants to expunge charges from their record.

    Attributes:
        name: A string that specifies client's name.
        dob: A datetime.date that specifies date of birth.
        cases: A list of Case(s).
    """
    def __init__(self, name, dob, cases):
        self.name = name
        self.dob = date2obj(dob)
        self.cases = cases

    def setCases(self,cases):
        self.cases = cases

    def num_charges(self):
        num = 0
        for case in self.cases:
            num += case.num_charges()
        return num

# class Client(object):
#     """ Client - An individual who wants to expunge charges from their record.
#
#     Attributes:
#         name: A string that specifies client's name.
#         dob: A datetime.date that specifies date of birth.
#         cases: A list of Case(s).
#     """
#     def __init__(self, name, dob, cases):
#         self.name = name
#         self.dob = dob
#         self.cases = cases
#
#     def num_charges(self):
#         num = 0
#         for case in self.cases:
#             num += case.num_charges()
#         return num
