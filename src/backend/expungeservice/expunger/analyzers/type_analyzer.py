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

        elif charge.type == 'Marijuana Ineligible':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.226')

        elif charge.type == 'List B':
            charge.expungement_result.set_reason('Further Analysis Needed')

        elif charge.type == 'Crime against person' or charge.type == '800 Level Traffic crime' or charge.type == 'Parking ticket':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.225(5)')

        elif charge.type == 'Schedule 1 PCS':
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(C)')

        elif charge.type == 'Non-Traffic Violation':
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(d)')

        elif charge.type == 'Felony Class C' or charge.type == 'Misdemeanor' in charge.level:
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(b)')

        elif charge.level == 'Felony Class B':
            self.class_b_felonies.append(charge)
            charge.expungement_result.set_reason('Further Analysis Needed')

        elif charge.level == 'Felony Class A':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.225(5)')

        else:
            charge.expungement_result.set_reason('Examine')
