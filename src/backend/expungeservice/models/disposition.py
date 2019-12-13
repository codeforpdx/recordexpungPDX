from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(eq=False)
class Disposition:
    date: Optional[date]
    ruling: str

    def __init__(self, date: Optional[str] = None, ruling: str = ""):
        self.date = self.__set_date(date)
        self.ruling = ruling

    def __set_date(self, date):
        if date:
            return datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        return None
