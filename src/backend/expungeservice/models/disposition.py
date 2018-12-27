import enum

class Disposition:

    def __init__(self):
        self.date = None
        self.ruling = None


# DispositionType = enum.Enum('Disposition',
#                             ' '.join([
#                                 'CONVICTION',
#                                 'NO_CONVICTION',
#                                 'DISMISSED',
#                                 'ACQUITTED',
#                                 'NO_COMPLAINT'
#                                 ]))
#
# class Disposition(object):
#     """ Disposition for a charge.
#
#     Attributes:
#         type_: An enum of type DispositionType.
#         date: A datetime.date specifying the date of the disposition.
#     """
#     def __init__(self, type_, date):
#         self.type_ = type_
#         self.date = date
