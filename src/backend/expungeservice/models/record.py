from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge


@dataclass(frozen=True)
class Alias:
    first_name: str
    last_name: str
    middle_name: str
    birth_date: str


@dataclass
class QuestionSummary:
    ambiguous_charge_id: str
    case_number: str
    root: Question


@dataclass
class Question:
    text: str
    options: Dict[str, Answer]
    selection: str = ""


@dataclass
class Answer:
    question: Optional[Question] = None
    edit: Optional[Dict[str, str]] = None


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
            total += case.summary.balance_due_in_cents

        return round(total / 100.0, 2)
