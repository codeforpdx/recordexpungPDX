class TypeAnalyzer:

    def evaluate(self, charges):
        if charges[0].disposition.ruling == 'Dismissed' or charges[0].disposition.ruling == 'Acquitted' or charges[0].disposition.ruling == 'No Complaint':
            charges[0].expungement_result.set_type_eligibility(True)
            charges[0].expungement_result.set_reason('Eligible under 137.225(1)(b)')

        elif charges[0].level == 'Felony Class C' or charges[0].level == 'Misdemeanor Class C':
            charges[0].expungement_result.set_type_eligibility(True)
            charges[0].expungement_result.set_reason('Eligible under 137.225(5)(b)')
