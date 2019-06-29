import re

from expungeservice.models.charge_types.base_charge import BaseCharge


class Charge:
    classification = None

    @classmethod
    def create(cls, **kwargs):
        cls.classification = None
        statute = Charge.__strip_non_alphanumeric_chars(kwargs['statute'])
        level = kwargs['level']
        section = Charge.__set_section(statute)
        Charge._set_classification(statute, level, section)
        kwargs['section'] = section
        kwargs['statute'] = statute
        kwargs['classification'] = cls.classification
        return BaseCharge(**kwargs)

    @classmethod
    def _set_classification(cls, statute, level, section):
        Charge._set_classification_by_statute(statute, section)
        if not cls.classification:
            Charge._set_classification_by_level(level)
        if not cls.classification:
            cls.classification = 'Unclassified'

    @staticmethod
    def _set_classification_by_statute(statute, section):
        Charge._marijuana_ineligible(statute, section)
        Charge._list_b(section)
        Charge._crime_against_person(section)
        Charge._traffic_crime(statute)
        Charge._parking_ticket(statute)
        Charge._schedule_1_pcs(section)

    @staticmethod
    def _set_classification_by_level(level):
        Charge._non_traffic_violation(level)
        Charge._misdemeanor(level)
        Charge._felony_class_c(level)
        Charge._felony_class_b(level)
        Charge._felony_class_a(level)

    @classmethod
    def _marijuana_ineligible(cls, statute, section):
        ineligible_statutes = ['475B359', '475B367', '475B371', '167262']
        if statute == '475B3493C' or section in ineligible_statutes:
            cls.classification = 'Marijuana Ineligible'

    @classmethod
    def _list_b(cls, section):
        ineligible_statutes = ['163200', '163205', '163575', '163535', '163175', '163275', '162165', '163525', '164405',
                               '164395', '162185', '166220', '163225', '163165']
        if section in ineligible_statutes:
            cls.classification = 'List B'

    @classmethod
    def _crime_against_person(cls, section):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        if section.isdigit() and any(int(section) in statute_range for statute_range in statute_ranges):
            cls.classification = 'Crime against person'

    @classmethod
    def _traffic_crime(cls, statute):
        statute_range = range(801, 826)
        if statute[0:3].isdigit() and int(statute[0:3]) in statute_range:
            cls.classification = '800 Level Traffic crime'

    @classmethod
    def _parking_ticket(cls, statute):
        statute_range = range(1, 100)
        if statute.isdigit() and int(statute) in statute_range:
            cls.classification = 'Parking ticket'

    @classmethod
    def _schedule_1_pcs(cls, section):
        if section in ['475854', '475874', '475884', '475894']:
            cls.classification = 'Schedule 1 PCS'

    @classmethod
    def _non_traffic_violation(cls, level):
        if 'Violation' in level:
            cls.classification = 'Non-Traffic Violation'

    @classmethod
    def _misdemeanor(cls, level):
        if 'Misdemeanor' in level:
            cls.classification = 'Misdemeanor'

    @classmethod
    def _felony_class_c(cls, level):
        if level == 'Felony Class C':
            cls.classification = 'Felony Class C'

    @classmethod
    def _felony_class_b(cls, level):
        if level == 'Felony Class B':
            cls.classification = 'Felony Class B'

    @classmethod
    def _felony_class_a(cls, level):
        if level == 'Felony Class A':
            cls.classification = 'Felony Class A'

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r'[^a-zA-Z0-9*]', '', statute).upper()

    @staticmethod
    def __set_section(statute):
        statute = Charge.__strip_non_alphanumeric_chars(statute)
        if len(statute) < 6:
            return ''
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
