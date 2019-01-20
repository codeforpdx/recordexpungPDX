from expungeservice.crawler.models.disposition import Disposition


class Charge:

    def __init__(self, name, statute, level, date):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = date
        self.disposition = Disposition()
