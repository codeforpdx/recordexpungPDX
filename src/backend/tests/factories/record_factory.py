from expungeservice.models.record_object import Record
from expungeservice.models.charge import Charge

class RecordFactory:

    @staticmethod
    def create(cases):
        return Record(list(cases))
