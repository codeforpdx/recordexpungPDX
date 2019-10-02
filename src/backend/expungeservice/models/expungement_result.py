class ExpungementResult:

    def __init__(self):
        self.type_eligibility = None
        self.type_eligibility_reason = ''
        self.time_eligibility = None
        self.time_eligibility_reason = ''
        self.date_of_eligibility = None

    def set_type_eligibility(self, type_eligibility):
        self.type_eligibility = type_eligibility

    def set_reason(self, reason):
        self.type_eligibility_reason = reason

    def __dict__(self):
        return {
            "type_eligibility": self.type_eligibility,
            "type_eligibility_reason": self.type_eligibility_reason,
            "time_eligibility": self.time_eligibility,
            "time_eligibility_reason": self.time_eligibility,
            "date_of_eligibility": self.date_of_eligibility
        }