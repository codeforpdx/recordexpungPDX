class ExpungementResult:

    def __init__(self):
        self.type_eligibility = None
        self.reason = ''
        self.time_eligibility = None
        self.time_eligibility_reason = ''
        self.date_of_eligibility = None

    def set_type_eligibility(self, type_eligibility):
        self.type_eligibility = type_eligibility

    def set_reason(self, reason):
        self.reason = reason
