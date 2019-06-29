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

        elif charge.type == 'MarijuanaIneligible':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.226')

        elif charge.type == 'ListB':
            charge.expungement_result.set_reason('Further Analysis Needed')

        elif charge.type == 'PersonCrime' or charge.type == 'Level800TrafficCrime' or charge.type == 'ParkingTicket':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.225(5)')

        elif charge.type == 'Schedule1PCS':
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(C)')

        elif charge.type == 'NonTrafficViolation':
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(d)')

        elif charge.type == 'FelonyClassC' or charge.type == 'Misdemeanor' in charge.level:
            charge.expungement_result.set_type_eligibility(True)
            charge.expungement_result.set_reason('Eligible under 137.225(5)(b)')

        elif charge.type == 'FelonyClassB':
            self.class_b_felonies.append(charge)
            charge.expungement_result.set_reason('Further Analysis Needed')

        elif charge.type == 'FelonyClassA':
            charge.expungement_result.set_type_eligibility(False)
            charge.expungement_result.set_reason('Ineligible under 137.225(5)')

        elif charge.type == 'UnclassifiedCharge':
            charge.expungement_result.set_reason('Examine')
