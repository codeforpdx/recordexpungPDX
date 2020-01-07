from dataclasses import dataclass, field
from typing import List, Optional
from more_itertools import padnone, take

from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.felony_class_b import FelonyClassB


@dataclass
class ChargesWithSummary:
    """
    most_recent_conviction: Most recent conviction if one exists from within the last ten years
    second_most_recent_conviction: Second most recent conviction if one exists from within the last ten years
    most_recent_dismissal: Most recent dismissal if one exists from within the last three years
    class_b_felonies: A list of class B felonies; excluding person crimes or firearm crimes
    most_recent_charge: The most recent charge within the last 20yrs; excluding traffic violations # (NB Kent): Why within the last 20yrs?
    """
    charges: List[Charge]
    acquittals: List[Charge] = field(default_factory=list)
    convictions: List[Charge] = field(default_factory=list)
    unknowns: List[Charge] = field(default_factory=list)
    old_convictions: List[Charge] = field(default_factory=list)
    most_recent_dismissal: Optional[Charge] = None
    most_recent_conviction: Optional[Charge] = None
    second_most_recent_conviction: Optional[Charge] = None
    most_recent_charge: Optional[Charge] = None
    class_b_felonies: List[Charge] = field(default_factory=list)


class ChargesSummarizer:
    @staticmethod
    def summarize(charges: List[Charge]) -> ChargesWithSummary:
        acquittals, convictions, unknowns = ChargesSummarizer._categorize_charges(charges)
        recent_convictions, old_convictions = ChargesSummarizer._categorize_convictions_by_recency(convictions)
        most_recent_dismissal = ChargesSummarizer._most_recent_dismissal(acquittals)
        most_recent_conviction, second_most_recent_conviction = ChargesSummarizer._most_recent_convictions(recent_convictions)
        most_recent_charge = ChargesSummarizer._most_recent_charge(charges)
        class_b_felonies = ChargesSummarizer._class_b_felonies(charges)
        return ChargesWithSummary(charges, acquittals, convictions, unknowns, old_convictions, most_recent_dismissal, most_recent_conviction, second_most_recent_conviction, most_recent_charge, class_b_felonies)

    @staticmethod
    def _categorize_charges(charges):
        acquittals, convictions, unknowns = [], [], []
        for charge in charges:
            if charge.acquitted():
                acquittals.append(charge)
            elif charge.convicted():
                convictions.append(charge)
            else:
                unknowns.append(charge)
        return acquittals, convictions, unknowns

    @staticmethod
    def _categorize_convictions_by_recency(convictions):
        recent_convictions = []
        old_convictions = []
        for charge in convictions:
            if charge.recent_conviction():
                recent_convictions.append(charge)
            else:
                old_convictions.append(charge)
        return recent_convictions, old_convictions

    @staticmethod
    def _most_recent_dismissal(acquittals):
        acquittals.sort(key=lambda charge: charge.date)
        if acquittals and acquittals[-1].recent_acquittal():
            return acquittals[-1]
        else:
            return None

    @staticmethod
    def _most_recent_convictions(recent_convictions):
        recent_convictions.sort(key=lambda charge: charge.disposition.date, reverse=True)
        first, second, third = take(3, padnone(recent_convictions))
        if first and "violation" in first.level.lower():
            return second, third
        elif second and "violation" in second.level.lower():
            return first, third
        else:
            return first, second

    @staticmethod
    def _most_recent_charge(charges):
        charges.sort(key=lambda charge: charge.disposition.date, reverse=True)
        if charges:
            return charges[0]
        else:
            return None

    @staticmethod
    def _class_b_felonies(charges):
        class_b_felonies = []
        for charge in charges:
            if isinstance(charge, FelonyClassB):
                class_b_felonies.append(charge)
        return class_b_felonies
