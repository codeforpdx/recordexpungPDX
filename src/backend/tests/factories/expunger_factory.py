from expungeservice.expunger import Expunger
from expungeservice.models.record import Record


class ExpungerFactory:
    @staticmethod
    def create():
        return Expunger(Record([]))
