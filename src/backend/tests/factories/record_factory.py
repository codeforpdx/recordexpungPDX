from expungeservice.models.record import Record

class RecordFactory:

    @staticmethod
    def create(cases):
        return Record(list(cases))
