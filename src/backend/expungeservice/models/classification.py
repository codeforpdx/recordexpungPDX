class Classification(object):
    """ Crime Level.

    Describes crime level. e.g. Felony Class A.

    Attributes:
        type_: A string describing the type of crime.
        class_: A string of length 1 specifying the class.

        #todo: I'm pretty sure that type can only be one of these: "Felony", "Misdemeanor", "Infraction" so lets do something about that

    """
    def __init__(self, type_, class_):
        self.type_ = type_
        self.class_ = class_

    def __str__(self):
        return '{} Class {}'.format(self.type_, self.class_)
