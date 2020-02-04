from dataclasses import dataclass, field
from typing import List

from expungeservice.models.case import Case
from expungeservice.models.charge import Charge


@dataclass
class Record:
    cases: List[Case]
    errors: List[str] = field(default_factory=list)

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
            total += case.get_balance_due_in_cents()

        return round(total / 100.0, 2)
