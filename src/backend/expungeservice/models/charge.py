import re
import sys

from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.level_800_traffic_crime import Level800TrafficCrime
from expungeservice.models.charge_types.list_b import ListB
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_crime import PersonCrime
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge


class Charge:
    classification = None

    @classmethod
    def create(cls, **kwargs):
        cls.classification = None
        statute = Charge.__strip_non_alphanumeric_chars(kwargs['statute'])
        level = kwargs['level']
        chapter = Charge._set_chapter(kwargs['statute'])
        section = Charge.__set_section(statute)
        Charge._set_classification(statute, level, chapter, section)
        kwargs['chapter'] = chapter
        kwargs['section'] = section
        kwargs['statute'] = statute
        return Charge._to_class(cls.classification)(**kwargs)

    @classmethod
    def _set_classification(cls, statute, level, chapter, section):
        Charge._set_classification_by_statute(statute, chapter, section)
        if not cls.classification:
            Charge._set_classification_by_level(level)
        if not cls.classification:
            cls.classification = 'UnclassifiedCharge'

    @staticmethod
    def _set_classification_by_statute(statute, chapter, section):
        Charge._marijuana_ineligible(statute, section)
        Charge._list_b(section)
        Charge._crime_against_person(section)
        Charge._traffic_crime(statute)
        Charge._parking_ticket(statute, chapter)
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
            cls.classification = 'MarijuanaIneligible'

    @classmethod
    def _list_b(cls, section):
        ineligible_statutes = ['163200', '163205', '163575', '163535', '163175', '163275', '162165', '163525', '164405',
                               '164395', '162185', '166220', '163225', '163165']
        if section in ineligible_statutes:
            cls.classification = 'ListB'

    @classmethod
    def _crime_against_person(cls, section):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        if section.isdigit() and any(int(section) in statute_range for statute_range in statute_ranges):
            cls.classification = 'PersonCrime'

    @classmethod
    def _traffic_crime(cls, statute):
        statute_range = range(801, 826)
        if statute[0:3].isdigit() and int(statute[0:3]) in statute_range:
            cls.classification = 'Level800TrafficCrime'

    @classmethod
    def _parking_ticket(cls, statute, chapter):
        statute_range = range(1, 100)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                cls.classification = 'ParkingTicket'
        elif statute.isdigit() and int(statute) in statute_range:
            cls.classification = 'ParkingTicket'

    @classmethod
    def _schedule_1_pcs(cls, section):
        if section in ['475854', '475874', '475884', '475894']:
            cls.classification = 'Schedule1PCS'

    @classmethod
    def _non_traffic_violation(cls, level):
        if 'Violation' in level:
            cls.classification = 'NonTrafficViolation'

    @classmethod
    def _misdemeanor(cls, level):
        if 'Misdemeanor' in level:
            cls.classification = 'Misdemeanor'

    @classmethod
    def _felony_class_c(cls, level):
        if level == 'Felony Class C':
            cls.classification = 'FelonyClassC'

    @classmethod
    def _felony_class_b(cls, level):
        if level == 'Felony Class B':
            cls.classification = 'FelonyClassB'

    @classmethod
    def _felony_class_a(cls, level):
        if level == 'Felony Class A':
            cls.classification = 'FelonyClassA'

    @staticmethod
    def _to_class(name):
        return getattr(sys.modules[__name__], name)

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
