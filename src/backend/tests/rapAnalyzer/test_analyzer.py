import unittest

import logging as log #this is used to print info to console for debugging purposes

log.basicConfig(level=log.DEBUG)

from expungeservice.analyzer.analyze import *
from expungeservice.analyzer.ineligible_crimes_list import *

from tests.fixtures.john_doe import JohnDoe # this is the pre downloaded john doe record in HTML format
from expungeservice.crawler.parsers.record_parser import RecordParser

from objbrowser import browse #import the object browser ui


import expungeservice.models.client as Client
import expungeservice.models.case as Case
import expungeservice.models.charge as Charge
import expungeservice.models.classification as Classification
import expungeservice.models.disposition as Disposition
import expungeservice.models.statute as Statute


def MakeClientObject(verbose = True):

    """

    This script should take data from the parser and turn it into a client rapsheet object

    """

    #todo: make this conform to formatting standards of the project




    parser = RecordParser()  #initialize the record parser
    parser.feed(JohnDoe.RECORD)  #Feed our example rap sheet into the parser (client name john doe)


    #   ***********
    #   *********** step 0: we manually inspect the parser object and marvel at its complexity and construction
    #   ***********
    browse(parser)




    #   ***********
    #   *********** step 1: create our client
    #   ***********

    # we take our client's info from the first case on the rap sheet
    # #todo: this logic seems sketchy
    # #todo: maybe verify that all cases are from the client name

    ClientName = parser.cases[0].name
    ClientDOB = parser.cases[0].birth_year #todo: refactor "birth_year"
    ClientsCases = []

    myClient  = Client(ClientName, ClientDOB, ClientsCases)

    browse(myClient)


    #   ***********
    #   *********** step 2: use parsed case data to create case objects
    #   ***********

    for case in parser.cases:           #iterate through cases

        browse(case)

        log.info('### Case number: ' + case.case_number)
        log.info('### Current status ' + case.current_status)
        log.info('### violation type ' + case.violation_type)

        for charge in case.charges:                 #iterate through each charge in the case
            log.info(">>> charge :" + charge)

            newCharge = Charge(charge)


        newCase = Case(case.case_number, case.citation_number, case.date, case.location, case.violation_type,
                       case.current_status, )





    #ourClient = Client(ClientName, ClientDOB, ClientCases)




if __name__ == '__main__':

    print("testing analyserr")
    MakeClientObject()





