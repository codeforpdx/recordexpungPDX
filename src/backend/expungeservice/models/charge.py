import re
import sys

from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
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
from expungeservice.models.charge_classifier import ChargeClassifier


class Charge:
    @classmethod
    def create(cls, **kwargs):
        case = kwargs['case']
        statute = Charge.__strip_non_alphanumeric_chars(kwargs['statute'])
        level = kwargs['level']
        chapter = Charge._set_chapter(kwargs['statute'])
        section = Charge.__set_section(statute)
        cls.classification = ChargeClassifier(case, statute, level, chapter, section).classify()
        kwargs['chapter'] = chapter
        kwargs['section'] = section
        kwargs['statute'] = statute
        return Charge._to_class(cls.classification)(**kwargs)

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
