class TypeAnalyzer:

    def __init__(self):
        self.class_b_felonies = []

    def evaluate(self, charges):
        for charge in charges:
            self.__evaluate(charge)

    def __evaluate(self, charge):
        if charge.type == 'FelonyClassB':
            self.class_b_felonies.append(charge)
