class Record:

    def __init__(self, list_cases):
        self.cases = list_cases
        self.errors = []

    @property
    def charges(self):
        list_charges = []

        for case in self.cases:
            list_charges.extend(case.charges)

        return list_charges

    @property
    def total_balance_due(self):
        total = 0

        for case in self.cases:
            total += case.get_balance_due()

        return round(total, 2)
