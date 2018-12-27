

import logging as log
log.basicConfig(level=log.DEBUG)

from tests.fixtures.john_doe import JohnDoe # this is the pre downloaded john doe record in HTML format
from tests.fixtures.case_details import CaseDetails # this is the case details of the first case in john doe's record

from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser

from objbrowser import browse #import the object browser ui

from expungeservice.models.client import Client
from expungeservice.models.charge import Charge



def BuildClientObject(clientsRecordPageHTML):

    """

    This script should take data from the parser and turn it into a client rapsheet object
    the reason for this function is to fill out the details of each charges since the record parser can't do that

    in theory this should work as such:

        0. something calls this function with a link to a case page.
        1. We parse the clients's record page with the RECORD PARSER
        2. then we lookup the detail page for each case  mentioned in the clients record, and then parse each one with the CASE PARSER
        3 ???

    we currently lack enough testing data to fully test this but we shall parse john doe's RECORD and the details of his first CASE
    #todo: more testing data

    since we only have details for the first case:
        this prototype will pretend that john doe only has one case

    """

    #todo: make this conform to formatting standards of the project

    # set up record parser
    recordparser = RecordParser()  #initialize the record parser

    #set up case parser
    caseparser = CaseParser()


    #   *********** step 1: lookup clients record and parse it. (record parser)


    recordparser.feed(clientsRecordPageHTML)  # Feed our example rap sheet into the parser (client name john doe)

    ClientName = recordparser.cases[0].name
    ClientDOB = recordparser.cases[0].birth_year #todo: this is not correct, DOB must come from the front end?
    ClientCases = recordparser.cases

    #browse(recordparser)

    #   *********** step 2: fill in the missing details in the charge and statute objects with data from case detail page (case parser)

    updatedCaseList = [] #initialize list of cases, this will be filled with the properly filled case info

    for case in ClientCases:

        print("Downloading case: " + case.case_number + " " + case.case_detail_link)

        # todo:  building case list code goes here
        # todo: iterate through list of detail page links

        caseRawData = CaseDetails.CASE_X1 #todo: actual list of case detail page data goes here
        caseparser.feed(caseRawData) #todo: iterator goes here

        ChargeList = [] #initialize empty list of charges

        for charge, contents in caseparser.hashed_charge_data.items(): #iterate through dict of hashed charge data

            ruling = caseparser.hashed_dispo_data[charge]['ruling'] # pull the ruling from the dispo data                   warning: this assumes that the charges and their corresponding dispo data are always indexed in the same order

            newCharge = Charge(contents['name'], contents['statute'], contents['level'], contents['date'], ruling)  #create charge object with the full details

            ChargeList.append(newCharge)

        case.setCharges(ChargeList) #update charge object with completed list of charges from detail parser
        updatedCaseList.append(case)


    return Client(ClientName, ClientDOB, updatedCaseList)

