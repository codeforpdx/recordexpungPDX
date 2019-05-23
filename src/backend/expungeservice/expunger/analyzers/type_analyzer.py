class TypeAnalyzer:

    def __init__(self):
        self.class_b_felonies = []

    def evaluate(self, charges):
        for charge in charges:
            self.__evaluate(charge)

    def __evaluate(self, charge):
        if charge.acquitted():
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(1)(b)')

        elif charge.marijuana_ineligible():
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.226')

        elif charge.list_b():
            charge.expungement_result.set_reason('Further Analysis Needed')

        elif charge.ineligible_under_137_225_5():
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.225(5)')

        elif charge.possession_sched_1():
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(C)')

        elif charge.non_traffic_violation():
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(d)')

        elif charge.level == 'Felony Class C' or 'Misdemeanor' in charge.level:
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(b)')

        elif charge.level == 'Felony Class B':
            self.class_b_felonies.append(charge)
            charge.expungement_result.set_reason('Further Analysis Needed')

        else:
            charge.expungement_result.set_reason('Examine')
