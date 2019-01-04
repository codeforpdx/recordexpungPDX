#!/usr/bin/env python3

from expungeservice.models.client import *
from expungeservice.models.statute import *
from expungeservice.models.disposition import *
from expungeservice.models.case import *
from expungeservice.models.charge import *
from expungeservice.models.crime_level import *
from expungeservice.analyzer.ineligible_crimes_list import *

from datetime import datetime
from datetime import timedelta


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

    """
    137.225(5) mandates the following

    class A felony
    sex crime from list A
    traffic crimes

    are not expunged
    """

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

    # def _is_charge_in_statute_list(charge, statutes, desc):
    #     check = ('Does the charge fall under any of these statutes: ' +
    #              ','.join(str(statute) for statute in statutes))
    #     # TODO implement this
    #     return CheckResult(check=check, result=False, check_desc=desc)

    # def _is_charge_sex_crime(charge):
    #     _statutes_sex_crimes = []
    #     return
    #
    # def _is_charge_traffic_crime(charge):
    #     # TODO update
    #     _statutes_traffic_crimes = []
    #     return RecordAnalyzer._is_charge_in_statute_list(
    #         charge, _statutes_traffic_crimes, 'Is the charge a traffic crime')

    def is_crime_on_list_B(charge):

        print("analyzing: " + charge.statute)

        for item in CrimesListB:

            if item == charge.statute:
                print('item is list B ' + item)
                return [True, item]

        print(charge.statute + " item is NOT list B")
        return False

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
    Analyze which records are expungeable

    The method sets the Charge instance's result attribute with type eligibility
    analysis result.

    Returns:
        A tuple consisting of:
            - A Result instance that describes the Time Eligibility analysis.
    """

    def analyze(self): #todo: implement time eligibility and conform to the comment above

        for case in self.client.cases:
            for charge in case.charges:

                #check type eligibility
                result = self.type_eligibility(charge)

                if result[0] == True:
                    print("Passed Type Eligibility tree: " + charge.name + " " + result[1])
                else:
                    print("failed Type Eligibility tree: " + charge.name + " " + result[1])


    """
    these are helper functions for analyze
    """
    def is_crime_list_B(charge):

        #print("analyzing: " + charge.statute.__str__())

        for item in CrimesListB:

            if item == charge.statute:
                return True

        #print(charge.statute.__str__() + " item is NOT list B")
        return False

    def is_crime_list_A(charge):
        print("analyzing: " + charge.statute.__str__())

        for item in CrimesListA:

            if len(item) == 2 and isinstance(object, (list,)):  # if this is a range of values

                lower_chapter = item[0][0:3]
                lower_subchapter = item[0][4:7]

                upper_chapter = item[1][0:3]
                upper_subchapter = item[1][4:7]

                if charge.statute.chapter <= upper_chapter and charge.statute.chapter >= lower_chapter:
                    if charge.statute.subchapter <= upper_subchapter and charge.statute.subchapter >= lower_subchapter:
                        #print(charge.statute.__str__() + " is NOT on list A")
                        return True  # return false and the reason why its false

        return True

    def is_charge_PCS_schedule_1(charge):
        if charge.name == "PCS": #todo: this is broken, find how to identify  this charge
            return True

    def is_charge_traffic_violation(charge):
        if charge.statute.chapter == "800":
            return True

    def is_charge_level_violation( charge):
        if charge.level.type_ == "VIOLATION":
            return True

    def is_charge_misdemeanor( charge):
        if charge.level.type_ == "MISDEMEANOR":
            return True

    def is_charge_felony_class_C( charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "C":
            return True

    def is_charge_felony_class_B(charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "B":
            return True

    def is_charge_felony_class_A( charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "A":
            return True

    def does_record_contain_arrest_or_conviction_in_last_20_years(client):
        for case in client.cases:
            for charge in case.charges:

                #todo: check for arrests within this time period

                if charge.disposition.type_ == "CONVICTED":

                    twenty_years_ago_date = datetime.today() - timedelta(days=(365*20)) #calculate time delta for twenty years ago #todo: calculate if this is accurate to within +-1

                    if twenty_years_ago_date.date() < charge.charge_date:
                        return True

        return False

    def is_charge_more_than_1_year_old(self, charge):

        one_year_ago_date = datetime.today() - timedelta(days=(365)) #calculate time delta for twenty years ago #todo: calculate if this is accurate to within +-1

        if one_year_ago_date.date() < charge.charge_date:
            return True
        else:
            return False

    def is_charge_dismissal_or_aquittal(self, charge):
        if charge.disposition.type_== "DISMISSED" or charge.disposition.type_== "AQUITTED": #todo: i dont know if "AQUITTED" is a valid type
            return True

    def is_charge_no_complaint(self, charge):
        if charge.disposition.type_== "NO COMPLAINT": #todo: i dont know if "NO COMPLAINT" is a valid type or if its even in this object
            return True

    """
        Run Type Eligibility analysis on a charge

        Args:
            charge: A Charge instance

        Returns:
            A Result instance
        """

    def type_eligibility(self, charge):
        # analysis = []
        #
        # analysis.append(RecordAnalyzer.is_charge_felony_class_A(charge, 'FELONY', 'A'))
        # if analysis[-1].result:
        #     return ResultInElig_137_225_5(analysis=analysis)

        # analysis.append(RecordAnalyzer._is_charge_sex_crime(charge))
        # if analysis[-1].result:
        #     return ResultInElig_137_225_5(analysis=analysis)
        #
        # analysis.append(RecordAnalyzer._is_charge_traffic_crime(charge))
        # if analysis[-1].result:
        #     return ResultInElig_137_225_5(analysis=analysis)

        # analysis.append(RecordAnalyzer.is)

        # todo: convert the code i wrote below to return the kind of result shown above

        #type eligibility tree

        if RecordAnalyzer.is_charge_felony_class_A(charge):
            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_crime_list_A(charge):
            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_crime_list_B(charge):
            charge.analysis = True, "Further Analysis Needed" #todo: 'true' doesnt seem accurate enough
            return charge.analysis

        #positive eligibilty tree

        if RecordAnalyzer.is_charge_PCS_schedule_1(charge):
            charge.analysis = True, "Eligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_charge_level_violation(charge):

            if RecordAnalyzer.is_charge_traffic_violation(charge):
                charge.analysis = False, "Ineligible under 137.225(5)"
                return charge.analysis

            charge.analysis = True, "Eligible under 137.225(5)(d)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_misdemeanor(charge):
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_felony_class_C(charge):
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_felony_class_B(charge):
            if RecordAnalyzer.does_record_contain_arrest_or_conviction_in_last_20_years(self.client): #todo: this operation could maybe be pre computed and stored somewhere since this is kinda expensive, but maybe ill leave it since it rarely gets called.
                charge.analysis = False, "Ineligible under 137.225(5)(a)(A)(i)"
                return charge.analysis
            else:
                charge.analysis = True, "Further Analysis" #todo: i left this terse as to follow flow chart. should it be "Further Analysis Needed"?
                return charge.analysis

        elif RecordAnalyzer.is_charge_dismissal_or_aquittal(charge):
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_no_complaint(charge):
            if RecordAnalyzer.is_charge_more_than_1_year_old(charge):
                charge.analysis = True, "Eligible under 137.225(5)(b)"
                return charge.analysis

        elif RecordAnalyzer.is_charge_no_complaint(charge) == False:
            charge.analysis = True, "Examine" #todo: i left this terse as to follow flow chart. should it be "Further Analysis Needed"?
            return charge.analysis


