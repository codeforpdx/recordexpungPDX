from expungeservice.expunger.helper_functions import *
import json, jsonpickle

class Client(object):
    """ Client - An individual who wants to expunge charges from their record.

    Attributes:
        name: A string that specifies client's name.
        dob: A datetime.date that specifies date of birth.
        cases: A list of Case(s).
    """
    def __init__(self, name, dob, cases):
        self.name = name
        self.dob = date2obj(dob)
        self.cases = cases

    def setCases(self,cases):
        self.cases = cases

    def num_charges(self):
        num = 0
        for case in self.cases:
            num += case.num_charges()
        return num

    def __dict__(self): #converts lists of objects to lists of dicts

        case_list = []

        for case in self.cases:
            case_list.append(case.__dict__())

        return {'name': self.name,
                'dob': str(self.dob),
                'cases': case_list,
                'num_charges': self.num_charges()
                }

    def toJSON(self):
        serialized = jsonpickle.encode(self.__dict__())
        serialized = json.dumps(json.loads(serialized), indent=2)
        return serialized
        # print(yaml.dump(yaml.load(serialized), indent=2))