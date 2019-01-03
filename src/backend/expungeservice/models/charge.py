# class Charge:
#
#     def __init__(self, attrs):
#         self.name = attrs[0]
#         self.statute = attrs[1]  # TODO: statute will need to be a Statute object. Need clarification on its attrs.
#         self.level = attrs[2]
#         self.date = Charge.__date(attrs[3])
#         self.disposition = attrs[4]


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
            date = None,
            disposition = None):

        self.name = name
        self.statute = statute
        self.level = level
        self.date = date
        self.disposition = disposition

        self._result = None

        @property
        def type_elig_result(self):
            return self._result

        @type_elig_result.setter
        def type_elig_result(self, result):
            self._result = result

        self.type_eligible = False # this is going to be a bool that represents if this is expungable
        self.time_eligible = False

        #todo: add a method which checks this charge's statute against list A and List B
        #todo: add expungable now t/f

    # def type_eligible(self):
    #     if self.statute



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