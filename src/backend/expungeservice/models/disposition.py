from dataclasses import dataclass
from datetime import date
from enum import Enum


class DispositionStatus(str, Enum):
    CONVICTED = "Convicted"
    DISMISSED = "Dismissed"
    NO_COMPLAINT = "No Complaint"
    DIVERTED = "Diverted"
    UNRECOGNIZED = "Unrecognized"


@dataclass(frozen=True)
class Disposition:
    date: date
    ruling: str
    status: DispositionStatus
    amended: bool = False


class DispositionCreator:
    @staticmethod
    def create(date: date, ruling: str, amended: bool = False) -> Disposition:
        status = DispositionCreator.__build_status(ruling)
        return Disposition(date, ruling, status, amended)

    @staticmethod
    def __build_status(ruling_string):
        ruling = ruling_string.lower()
        conviction_rulings = ["convicted", "conviction", "reduced", "finding - guilty", "conversion", "converted", "bail forfeiture", ]
        dismissal_rulings = [
            "acquitted",
            "acquittal",
            "dismissed",
            "dismissal",
            "finding - not guilty",
            "accusatory instrument filed",
            "removed from charging instrument",
            "plea lesser charge",
        ]

        if any([rule in ruling for rule in conviction_rulings]):
            return DispositionStatus.CONVICTED

        elif any([rule in ruling for rule in dismissal_rulings]):
            return DispositionStatus.DISMISSED

        elif "diverted" in ruling:
            return DispositionStatus.DIVERTED

        elif "no complaint" in ruling:
            return DispositionStatus.NO_COMPLAINT

        else:
            return DispositionStatus.UNRECOGNIZED
