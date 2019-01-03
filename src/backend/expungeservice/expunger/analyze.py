#!/usr/bin/env python3

from expungeservice.models.client import *
from expungeservice.models.statute import *
from expungeservice.models.disposition import *
from expungeservice.models.case import *
from expungeservice.models.charge import *
from expungeservice.models.crime_level import *


import collections
import enum


class ResultCode(enum.Enum):
    INELIGIBLE = 'Ineligible'
    ELIGIBLE = 'Eligible'
    FURTHER_ANALYSIS = 'Further analysis needed'
    EXAMINE = 'Examine'
    NO_ACTION = 'Take no action'
    OPEN_CASE = 'Open Case'

"""
A class for storing individual analysis steps

Attributes:
    result: A boolean that's the result of the check
    check: A string that breifly describes the check
    check_desc: A string that elaborates the check (optional)
"""
CheckResult = collections.namedtuple('CheckResult', 'result check check_desc',
                                     defaults=[None])

class Result(object):
    """
    A class for storing analysis results

    Attributes:
        code: A ResultCode instance.
        statute: A Statute instance that's associated with arrived result.
        date: A datetime.date instance that specifies eligibility date.
        analysis: A list of CheckResult instances that describes the analysis done.
    """
    def __init__(self, code=None, analysis=None,
                 statute=None, date=None):
        self.code = code
        self.analysis = analysis
        self.statute = statute
        self.date = date

    def __str__(self):
        return ' '.join([str(self.code), str(self.analysis), str(self.statute), str(self.date)])

class ResultInElig_137_225_5(Result):
    def __init__(self, **kwargs):
        Result.__init__(self, code=ResultCode.INELIGIBLE,
                        statute=Statute(137, 225, 5), **kwargs)

class RecordAnalyzer(object):
    """
    A class for analyzing client's records

    Attributes:
        client: A Client instance
    """

    def __init__(self, client):
        self.client = client

    def _is_charge_level(charge, type_, class_):
        check = 'Is the charge a {}'.format(type_)
        if class_:
            check += ' class {}'.format(class_)

        result = (charge.level.type_ ==  type_ and
                  (not class_ or charge.level.class_ == class_))

        return CheckResult(check=check, result=result)

    def _is_charge_statute(charge, statute):
        check = 'Does the charge fall under statute: ' + str(statute)
        return CheckResult(check=check, result=charge.statute == statute)

    def _is_charge_in_statute_list(charge, statutes, desc):
        check = ('Does the charge fall under any of these statutes: ' +
                 ','.join(str(statute) for statute in statutes))
        # TODO implement this
        return CheckResult(check=check, result=False, check_desc=desc)

    def _is_charge_sex_crime(charge):
        # TODO update
        _statutes_sex_crimes = []
        return RecordAnalyzer._is_charge_in_statute_list(
            charge, _statutes_sex_crimes, 'Is the charge a sex crime')

    def _is_charge_traffic_crime(charge):
        # TODO update
        _statutes_traffic_crimes = []
        return RecordAnalyzer._is_charge_in_statute_list(
            charge, _statutes_traffic_crimes, 'Is the charge a traffic crime')

    def _have_open_case(self):
        check = 'Is there a open case for the client'
        result = any([case.state == CaseState.OPEN for case in self.client.cases])
        return CheckResult(check=check, result=result)

    """
    Run Time Eligibility analysis on the client and their records

    TODO: make it return analysis for each charge as well (which is supposed
    to be an update on eligibility date and relevan statutes)

    Returns:
        An Result instance
    """
    def time_eligibility(self):
        analysis = []

        analysis.append(self._have_open_case())
        if analysis[-1].result:
            return Result(ResultCode.OPEN_CASE, analysis)

        # TODO implement the rest

        return Result(ResultCode.NO_ACTION)

    """
    Run Type Eligibility analysis on a charge

    Args:
        charge: A Charge instance

    Returns:
        A Result instance
    """
    def type_eligibility(self, charge):
        analysis = []

        analysis.append(RecordAnalyzer._is_charge_level(charge, 'Felony', 'A'))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        analysis.append(RecordAnalyzer._is_charge_sex_crime(charge))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        analysis.append(RecordAnalyzer._is_charge_traffic_crime(charge))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        # TODO add remaining analysis

        return Result(ResultCode.FURTHER_ANALYSIS, analysis)

    """
    Analyze which records are expungeable

    The method sets the Charge instance's result attribute with type eligibility
    analysis result.

    Returns:
        A tuple consisting of:
            - A Result instance that describes the Time Eligibility analysis.
    """
    def analyze(self):
        for case in self.client.cases:
            for charge in case.charges:
                charge.type_elig_result = self.type_eligibility(charge)

        return self.time_eligibility()



    #todo: figure out if i can delete this ->

    # def is_crime_on_ineligible_list(statute):
    #     """
    #     Searches through list of discreet values and ranges
    #     to determine if a given statute is on the list of ineligible crimes
    #
    #     Args:
    #         statute  <---- a given statute number code
    #
    #     Returns:
    #         True Or False
    #
    #     """
    #
    #     statute = float(statute)
    #
    #     for item in IneligibleCrimesList:
    #         if type(item) == list:
    #             if statute >= float(item[0]) and statute <= float(item[1]):
    #                 return True
    #         else:
    #             if item == statute:
    #                 return True
    #
    #     return False

