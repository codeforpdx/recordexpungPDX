class TypeAnalyzer:

    def evaluate(self, charges):
        if charges[0].disposition.ruling == 'Dismissed' or charges[0].disposition.ruling == 'Acquitted':
            charges[0].expungement_result.set_type_eligibility(True)
            charges[0].expungement_result.set_reason('Eligible under 137.225(1)(b)')
