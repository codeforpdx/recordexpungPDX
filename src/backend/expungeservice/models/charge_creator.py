import re

from expungeservice.models.charge_classifier import ChargeClassifier


class ChargeCreator:
    @staticmethod
    def create(**kwargs):
        case = kwargs['case']
        statute = ChargeCreator.__strip_non_alphanumeric_chars(kwargs['statute'])
        level = kwargs['level']
        chapter = ChargeCreator._set_chapter(kwargs['statute'])
        section = ChargeCreator.__set_section(statute)
        classification = ChargeClassifier(case.violation_type, statute, level, chapter, section).classify()
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
