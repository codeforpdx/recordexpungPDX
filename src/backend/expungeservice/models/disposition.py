import enum
import datetime

class Disposition(object):
    """ Disposition for a charge.

    Attributes:
        type_: An enum of type DispositionType.
        date: A datetime.date specifying the date of the disposition.
    """
    def __init__(self, type_, date=None):
        self.type_ = type_
        self.dispo_date = date

        # parse date into proper datetime object, if it is a string
        if type(self.dispo_date) == type(""):
            month, day, year = map(int, self.dispo_date.split("/"))
            self.dispo_date = datetime.date(year, month, day)

    def __dict__(self):
        return {'type': self.type_,
                'dispo_date': str(self.dispo_date)
                }


DispositionType = enum.Enum('Disposition',
                            ' '.join([
                                'CONVICTION',
                                'NO_CONVICTION',
                                'DISMISSED',
                                'ACQUITTED',
                                'NO_COMPLAINT'
                                ]))
