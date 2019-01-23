import re

from expungeservice.crawler.models.disposition import Disposition
from expungeservice.crawler.models.expungement_result import ExpungementResult


class Charge:

    def __init__(self, name, statute, level, date):
        self.name = name
        self.statute = Charge.__strip_non_alphanumeric_chars(statute)
        self.level = level
        self.date = date
        self.disposition = Disposition()
        self.expungement_result = ExpungementResult()

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r'[^a-zA-Z0-9*]', '', statute).upper()
