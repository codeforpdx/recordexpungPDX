from dataclasses import dataclass

from expungeservice.models.case import Case


@dataclass
class ChargeClassifier:
    case : Case
    statute : str
    level : str
    chapter : str
    section : str

    def classify(self):
        def classification_found(c):
            return c is not None

        for c in self.__classifications_list():
            if classification_found(c):
                return c

    def __classifications_list(self):
        yield ChargeClassifier._juvenile_charge(self.case)
        yield from ChargeClassifier._classification_by_statute(self.statute, self.chapter, self.section)
        yield ChargeClassifier._municipal_parking(self.case)
        yield from ChargeClassifier._classification_by_level(self.level)
        yield "UnclassifiedCharge"

    @staticmethod
    def _juvenile_charge(case):
        if 'juvenile' in case.violation_type.lower():
            return 'JuvenileCharge'

    @staticmethod
    def _classification_by_statute(statute, chapter, section):
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._list_b(section)
        yield ChargeClassifier._crime_against_person(section)
        yield ChargeClassifier._traffic_crime(statute)
        yield ChargeClassifier._parking_ticket(statute, chapter)
        yield ChargeClassifier._schedule_1_pcs(section)

    @staticmethod
    def _classification_by_level(level):
        yield ChargeClassifier._non_traffic_violation(level)
        yield ChargeClassifier._misdemeanor(level)
        yield ChargeClassifier._felony_class_c(level)
        yield ChargeClassifier._felony_class_b(level)
        yield ChargeClassifier._felony_class_a(level)

    @classmethod
    def _marijuana_ineligible(cls, statute, section):
        ineligible_statutes = ['475B359', '475B367', '475B371', '167262']
        if statute == '475B3493C' or section in ineligible_statutes:
            return 'MarijuanaIneligible'

    @classmethod
    def _list_b(cls, section):
        ineligible_statutes = ['163200', '163205', '163575', '163535', '163175', '163275', '162165', '163525', '164405',
                               '164395', '162185', '166220', '163225', '163165']
        if section in ineligible_statutes:
            return 'ListB'

    @classmethod
    def _crime_against_person(cls, section):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        if section.isdigit() and any(int(section) in statute_range for statute_range in statute_ranges):
            return 'PersonCrime'

    @classmethod
    def _traffic_crime(cls, statute):
        statute_range = range(801, 826)
        if statute[0:3].isdigit() and int(statute[0:3]) in statute_range:
            return 'Level800TrafficCrime'

    @classmethod
    def _parking_ticket(cls, statute, chapter):
        statute_range = range(1, 100)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                return 'ParkingTicket'
        elif statute.isdigit() and int(statute) in statute_range:
            return 'ParkingTicket'

    @classmethod
    def _schedule_1_pcs(cls, section):
        if section in ['475854', '475874', '475884', '475894']:
            return 'Schedule1PCS'

    @classmethod
    def _municipal_parking(cls, case):
        if 'parking' in case.violation_type.lower():
            return 'ParkingTicket'

    @classmethod
    def _non_traffic_violation(cls, level):
        if 'Violation' in level:
            return 'NonTrafficViolation'

    @classmethod
    def _misdemeanor(cls, level):
        if 'Misdemeanor' in level:
            return 'Misdemeanor'

    @classmethod
    def _felony_class_c(cls, level):
        if level == 'Felony Class C':
            return 'FelonyClassC'

    @classmethod
    def _felony_class_b(cls, level):
        if level == 'Felony Class B':
            return 'FelonyClassB'

    @classmethod
    def _felony_class_a(cls, level):
        if level == 'Felony Class A':
            return 'FelonyClassA'