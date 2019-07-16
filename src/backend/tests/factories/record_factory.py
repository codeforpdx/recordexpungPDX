from expungeservice.models.record_object import Record
from expungeservice.models.charge import Charge
from tests.factories.case_factory import CaseFactory


class RecordFactory:

    @staticmethod
    def create(cases):
        return Record(list(cases))
