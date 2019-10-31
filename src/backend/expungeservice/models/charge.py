import re

from expungeservice.models.charge_classifier import ChargeClassifier


class Charge:
    @staticmethod
    def create(**kwargs):
        case = kwargs['case']
        statute = Charge.__strip_non_alphanumeric_chars(kwargs['statute'])
        level = kwargs['level']
        chapter = Charge._set_chapter(kwargs['statute'])
        section = Charge.__set_section(statute)
        classification = ChargeClassifier(case, statute, level, chapter, section).classify()
        kwargs['chapter'] = chapter
        kwargs['section'] = section
        kwargs['statute'] = statute
        return classification(**kwargs)

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r'[^a-zA-Z0-9*]', '', statute).upper()

    @staticmethod
    def _set_chapter(statute):
        if '.' in statute:
            return statute.split('.')[0]
        else:
            return None

    @staticmethod
    def __set_section(statute):
        if len(statute) < 6:
            return ''
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
