from datetime import datetime


class Disposition:

    def __init__(self, date=None, ruling=None):
        self.date = self.__set_date(date)
        self.ruling = ruling

    def __set_date(self, date):
        if date:
            return datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        return None
