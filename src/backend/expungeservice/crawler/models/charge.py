class Charge:

    def __init__(self, attrs):
        self.name = attrs[0]
        self.statute = attrs[1]  # TODO: statute will need to be a Statute object. Need clarification on its attrs.
        self.level = attrs[2]
        self.date = Charge.__date(attrs[3])
        self.disposition = attrs[4]
