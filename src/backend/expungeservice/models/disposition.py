import enum
import datetime


DispositionType = enum.Enum('Disposition',
                            ' '.join([
                                'CONVICTED',
                                'NO_CONVICTION',
                                'DISMISSED',
                                'ACQUITTED',
                                'NO_COMPLAINT'
                                ]))

class Disposition(object):
    """ Disposition for a charge.

    Attributes:
        type_: An enum of type DispositionType.
        date: A datetime.date specifying the date of the disposition.
    """
    def __init__(self, type_, date_string=None, date=None):
        self.type_ = type_
        self.date = date
        self.date_string = date_string

        self.parse_date_string()

    def parse_date_string(self):
        # parse date into proper datetime object, if it is a string
        if type(self.date_string) == type(""):
            month, day, year = map(int, self.date_string.split("/"))
            self.date = datetime.date(year, month, day)

    def __dict__(self):
        return {'type': self.type_,
                'date_string': str(self.date_string)
                }


