class TypeAnalyzer:

    def evaluate(self, charges):
        if charges[0].disposition.ruling == 'Dismissed' or charges[0].disposition.ruling == 'Acquitted' or charges[0].disposition.ruling == 'No Complaint':
            charges[0].expungement_result.set_type_eligibility(True)
            charges[0].expungement_result.set_reason('Eligible under 137.225(1)(b)')

        elif TypeAnalyzer.__crime_against_person(charges):
            pass

        elif charges[0].level == 'Felony Class C' or charges[0].level == 'Misdemeanor Class C':
            charges[0].expungement_result.set_type_eligibility(True)
            charges[0].expungement_result.set_reason('Eligible under 137.225(5)(b)')

    @staticmethod
    def __crime_against_person(charges):
        statute = int(charges[0].statute[0:6])
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        return any(statute in statute_range for statute_range in statute_ranges)
