from dataclasses import dataclass, field
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
    status: DispositionStatus = field(init=False)

    def __init__(self, date: Optional[str] = None, ruling: str = ""):
        self.date = self.__set_date(date)
        self.ruling = ruling
        self.__post_init__()

    def __post_init__(self):
        self.status = self.__set_status()

    def __set_date(self, date):
        if date:
            return datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        return None

    def __set_status(self):
        ruling = self.ruling.lower()
        conviction_rulings = [
            "convicted", "conviction", "reduced",
            "finding - guilty","conversion", "converted"]
        dismissal_rulings = [
            "acquitted", "acquittal", "dismissed",
            "dismissal", "finding - not guilty"]

        if any([rule in ruling for rule in conviction_rulings]):
            return DispositionStatus.CONVICTED

        elif any([rule in ruling for rule in dismissal_rulings]):
            return  DispositionStatus.DISMISSED

        elif "diverted" in ruling:
            return  DispositionStatus.DIVERTED

        elif "no complaint" in ruling:
            return  DispositionStatus.NO_COMPLAINT

        else:
            return  DispositionStatus.UNKNOWN
