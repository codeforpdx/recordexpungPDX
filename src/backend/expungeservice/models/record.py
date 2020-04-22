from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge


@dataclass(frozen=True)
class Alias:
    first_name: str
    last_name: str
    middle_name: str
    birth_date: str


@dataclass
class Question:
    ambiguous_charge_id: str
    case_number: str
    question: str
    options: Dict[str, str]
    answer: str = ""


@dataclass(frozen=True)
class Record:
    cases: Tuple[Case, ...]
    errors: Tuple[str, ...] = ()

    @property
    def charges(self):
        list_charges: List[Charge] = []

        for case in self.cases:
            list_charges.extend(case.charges)

        return list_charges

    @property
    def total_balance_due(self):
        total = 0

        for case in self.cases:
            total += case.balance_due_in_cents

        return round(total / 100.0, 2)
