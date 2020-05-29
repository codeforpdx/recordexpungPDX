from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, ChargeType
from expungeservice.models.record import Record, Question

AmbiguousCharge = List[Charge]
AmbiguousCase = List[Case]
AmbiguousRecord = List[Record]


@dataclass
class AmbiguousChargeTypeWithQuestion:
    ambiguous_charge_type: List[ChargeType]
    question: Optional[Question] = None
