class ExpungementResult:

    def __init__(self):
        self.type_eligibility = None
        self.reason = ''

    def set_type_eligibility(self, type_eligibility):
        self.type_eligibility = type_eligibility

    def set_reason(self, reason):
        self.reason = reason
