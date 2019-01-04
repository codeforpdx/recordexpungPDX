#!/usr/bin/env python3

import logging

logging.basicConfig(level=logging.DEBUG)

from expungeservice.models.client import *
from expungeservice.models.statute import Statute
from expungeservice.models.disposition import *
from expungeservice.models.case import *
from expungeservice.models.charge import *
from expungeservice.models.crime_level import *
from expungeservice.analyzer.ineligible_crimes_list import *

from objbrowser import browse #import the object browser ui

from operator import attrgetter

from datetime import datetime
from datetime import timedelta


import collections
import enum



#todo: i am not sure if im supposed to be using getters and setters for objects python lets me just set object values however i want but i should probably do that


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

    # def is_crime_on_list_B(charge):
    #
    #     logging.info("analyzing: " + charge.statute)
    #
    #     for item in CrimesListB:
    #
    #         if item == charge.statute:
    #             return [True, item]
    #
    #     return False

    #todo: there is much duplication between the next three functions and everywhere cameron has been coding
    #todo: maybe instead of searching for equivalent charge objects we should just refer to the original charge object's memory address or whatever that thing is like <expungeservice.models.charge.Charge object at 0x7f1c637d9b38>

    #find most recent conviction

    def get_all_charges_sorted_by_date(self):
        chargelist = []

        for case in self.client.cases:
            for charge in case.charges:
                if charge.disposition.type_ == "CONVICTED":
                    chargelist.append(charge)

        sorted_list = sorted(chargelist, key=attrgetter('charge_date')) # sort list of convictions by date, note: the list is mostly sorted by the parser but not completely sorted so this is in fact necessary
        return sorted_list

    def get_mrc(self):
        """
        Returns: Most Recently Convicted Charge Object #todo: get_mrc should eventually return case info too. which probably means the charge object needs to know its parent case object
        """

        return RecordAnalyzer.get_all_charges_sorted_by_date(self)[-1:][0]

    def get_last_ten_years_of_convictions(self):
        RecordAnalyzer.get_all_charges_sorted_by_date(self)

    def is_mrc_time_eligible(self, mrc):




    def is_charge_time_eligible(self, charge, mrc):

        # calculate ten years from MRC
        ten_years_from_mrc = mrc.charge_date + timedelta(days=(365 * 10))  # calculate time delta for twenty years ago #todo: calculate if this is accurate to within +-1 day

        if datetime.today() > ten_years_from_mrc:
            logging.info(charge.name + " is time eligible since " + ten_years_from_mrc )
            charge.time_eligible = True
            charge.time_eligible_analysis = "Time eligible since " + str(ten_years_from_mrc)

        if datetime.today() < ten_years_from_mrc:
            logging.info(charge.name + " is not time eligible unitl " + ten_years_from_mrc)
            charge.time_eligible = True
            charge.time_eligible_analysis = "Ineligible under 137.225(7)(b). Time Eligiblity begins " + str(
                ten_years_from_mrc)

    def set_all_other_charges_to_ineligible_until(self, mrc):

        #todo: maybe rewrite this to say more intelligent things like, time eligible since....

        for case in self.client.cases:
            for charge in case.charges:
                if charge != mrc:
                    RecordAnalyzer.is_charge_time_eligible(charge, mrc) #this function sets the appropriate properties automatically

    def does_record_contain_conviction_from_last_ten_years(self):

        for case in self.client.cases:
            for charge in case.charges:
                if charge.disposition.type_ == "CONVICTED":

                    ten_years_ago = datetime.today() - timedelta(days=(365*10)) #calculate time delta for twenty years ago #todo: calculate if this is accurate to within +-1 day

                    if ten_years_ago.date() < charge.charge_date:
                        return True

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


        #check for any Open Cases
        analysis.append(self._have_open_case())
        if analysis[-1].result:
            return Result(ResultCode.OPEN_CASE, analysis)

        #check for any charges in last ten years
        if RecordAnalyzer.does_record_contain_conviction_from_last_ten_years(self):
            return False

        ass = RecordAnalyzer.get_mrc(self)

        self.set_all_other_charges_to_ineligible_until(ass)

        browse(self.client)






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

        self.time_eligibility()

        return None

        #iterate through all cases and charges to check type eligibility
        for case in self.client.cases:
            for charge in case.charges:

                logging.info("***************************************************************")
                logging.info("analyzing: " + charge.name + " " + charge.statute.__str__())

                if charge.statute.chapter == None: #todo: throw errror
                    logging.warning(charge.name)
                    logging.warning("error")

                result = self.type_eligibility(charge)

                if result[0] == True:
                    logging.info("Passed Type Eligibility tree: " + charge.name + " " + result[1])
                else:
                    logging.info("failed Type Eligibility tree: " + charge.name + " " + result[1])

    """
    these are helper functions for analyze
    """
    def is_crime_list_B(charge):

        for item in CrimesListB:

            if item == charge.statute:
                return True

        return False

    def is_crime_list_A(charge):

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

        return False

    def is_crime_driving_crime(charge):

        for item in DrivingCrimes:

            if len(item) == 2 and isinstance(object, (list,)):  # if this is a range of values

                lower_chapter = item[0][0:3]
                lower_subchapter = item[0][4:7]

                upper_chapter = item[1][0:3]
                upper_subchapter = item[1][4:7]

                if charge.statute.chapter <= upper_chapter and charge.statute.chapter >= lower_chapter:
                    if charge.statute.subchapter <= upper_subchapter and charge.statute.subchapter >= lower_subchapter:

                        #print(charge.statute.__str__() + " is NOT on list A")
                        return True  # return false and the reason why its false

        return False

    def is_crime_marijuana_list(charge):

        #todo: this wont work at all

        for item in MarijuanaIneligible:

            if item == charge.statute:
                return True

        return False

    def is_charge_PCS_schedule_1(charge):
        if charge.name == "PCS": #todo: this is broken, find how to identify  this charge
            return True

    def is_charge_traffic_violation(charge):

        if charge.statute.chapter == None: #todo: throw error
            return False

        if int(charge.statute.chapter) <= 900 and int(charge.statute.chapter) >= 800:
            return True
        return False

    def is_charge_level_violation( charge):
        if charge.level.type_ == "VIOLATION":
            return True
        return False

    def is_charge_misdemeanor( charge):
        if charge.level.type_ == "MISDEMEANOR":
            return True
        return False

    def is_charge_felony_class_C( charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "C":
            return True
        return False

    def is_charge_felony_class_B(charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "B":
            return True
        return False

    def is_charge_felony_class_A(charge):
        if charge.level.type_ == "FELONY" and charge.level.class_ == "A":
            return True
        return False


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
        return False

    def is_charge_dismissal_or_aquittal(charge):
        if charge.disposition.type_== "DISMISSED" or charge.disposition.type_== "AQUITTED": #todo: i dont know if "AQUITTED" is a valid type
            return True
        return False

    def is_charge_no_complaint(charge):
        if charge.disposition.type_== "NO COMPLAINT": #todo: i dont know if "NO COMPLAINT" is a valid type or if its even in this object
            return True
        return False

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

            logging.info('felony class A')

            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_crime_list_A(charge) == True:
            logging.info('crime list A')
            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_crime_driving_crime(charge) == True:
            logging.info('crime list Driving')
            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_crime_list_B(charge) == True:
            logging.info('crime list b')
            charge.analysis = True, "Further Analysis Needed" #todo: 'true' doesnt seem accurate enough
            return charge.analysis

        if RecordAnalyzer.is_crime_marijuana_list(charge) == True:  #todo: 'this  one is broken and will never be true
            logging.info('crime list marijuana')
            charge.analysis = True, "marijuana inelgibible"
            return charge.analysis

        #positive eligibilty tree

        if RecordAnalyzer.is_charge_PCS_schedule_1(charge) == True:
            logging.info('pcs 1')
            charge.analysis = True, "Eligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_charge_traffic_violation(charge) == True:
            logging.info('traffic violation')
            charge.analysis = False, "Ineligible under 137.225(5)"
            return charge.analysis

        if RecordAnalyzer.is_charge_level_violation(charge) == True:

            logging.info('non traffic violation')
            charge.analysis = True, "Eligible under 137.225(5)(d)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_misdemeanor(charge) == True:
            logging.info('misdemeanor')
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_felony_class_C(charge) == True:
            logging.info('felony class c')
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_felony_class_B(charge) == True:
            if RecordAnalyzer.does_record_contain_arrest_or_conviction_in_last_20_years(self.client): #todo: this operation could maybe be pre computed and stored somewhere since this is kinda expensive, but maybe ill leave it since it rarely gets called.
                logging.info('felony class B + conviction within 20 yrs')
                charge.analysis = False, "Ineligible under 137.225(5)(a)(A)(i)"
                return charge.analysis
            else:

                logging.info('felony class B + NO conviction within 20 yrs')
                charge.analysis = True, "Further Analysis" #todo: i left this terse as to follow flow chart. should it be "Further Analysis Needed"?
                return charge.analysis

        elif RecordAnalyzer.is_charge_dismissal_or_aquittal(charge) == True:
            logging.info('aquitted or dismissed')
            charge.analysis = True, "Eligible under 137.225(5)(b)"
            return charge.analysis

        elif RecordAnalyzer.is_charge_no_complaint(charge) == True: #todo: no complaint is not behaving properly
            if RecordAnalyzer.is_charge_more_than_1_year_old(charge) == True:
                logging.info('charge is no_complaint + older than 1 year')
                charge.analysis = True, "Eligible under 137.225(5)(b)"
                return charge.analysis

        elif RecordAnalyzer.is_charge_no_complaint(charge) == False:
            logging.info('no complaint')
            charge.analysis = True, "Examine" #todo: i left this terse as to follow flow chart. should it be "Further Analysis Needed"?
            return charge.analysis
        else:
            logging.info("it is nothing") #todo this should throw error



