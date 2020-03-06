from typing import List

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge
from expungeservice.models.record import Record

AmbiguousCharge = List[Charge]
AmbiguousCase = List[Case]
AmbiguousRecord = List[Record]
