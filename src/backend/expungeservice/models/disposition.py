from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from enum import Enum


class DispositionStatus(str, Enum):
    CONVICTED = "Convicted"
    DISMISSED = "Dismissed"
    NO_COMPLAINT = "No Complaint"
    DIVERTED = "Diverted"
    UNKNOWN = "Unknown"

@dataclass(eq=False)
class Disposition:
    date: Optional[date]
    ruling: str
    status: DispositionStatus

    def __init__(self, date: Optional[str] = None, ruling: str = ""):
        self.date = self.__set_date(date)
        self.ruling = ruling
        self.status = self.__set_status()

    def __set_date(self, date):
        if date:
            return datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        return None

    def __set_status(self):
        ruling = self.ruling.lower()
        if any([conviction_ruling in ruling for conviction_ruling in [
                "convicted",
                "conviction",
                "finding - guilty",
                "conversion",
                "converted"]]):

            return DispositionStatus.CONVICTED

        elif any([dismissal_ruling in ruling for dismissal_ruling in [
                "acquitted",
                "acquittal",
                "dismissed",
                "dismissal",
                "finding - not guilty"]]):

            return  DispositionStatus.DISMISSED

        elif "diverted" in ruling:

            return  DispositionStatus.DIVERTED

        elif "no complaint" in ruling:

            return  DispositionStatus.NO_COMPLAINT

        else:

            return  DispositionStatus.UNKNOWN
