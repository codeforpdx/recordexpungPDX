from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser

from objbrowser import browse #import the object browser ui

from expungeservice.models.client import Client
from expungeservice.models.charge import Charge

from tests.fixtures.ward_weaver import WardWeaver
from tests.fixtures.bill_sizemore import BillSizemore


"""this is only used when loading locally stored html files"""

def file2string(location):
    with open(location, 'r') as myfile:
        filedata = myfile.read()

    myfile.close()
    return filedata



def BuildClientObject(PathToExampleHTMLFiles, clientsRecordPageHTML):

    """

    This script should take data from the parser and turn it into a client rapsheet object
    the reason for this function is to fill out the details of each charges since the record parser can't do that

    in theory this should work as such:

        0. something calls this function with a link to a case page.
        1. We parse the clients's record page with the RECORD PARSER
        2. then we lookup the detail page for each case  mentioned in the clients record, and then parse each one with the CASE PARSER
        3 ???

    """

    #todo: make this conform to formatting standards of the project

    # set up record parser
    recordparser = RecordParser()  #initialize the record parser

    # lookup clients record and parse it. (record parser)
    recordparser.feed(clientsRecordPageHTML)  # Feed our example rap sheet into the parser (client name john doe)


    ClientName = recordparser.cases[0].name
    ClientDOB = recordparser.cases[0].birth_year #todo: this is not correct, DOB must come from the front end?
    ClientCases = recordparser.cases

    #fill in the missing details in the charge and statute objects with data from case detail page (case parser)
    updatedCaseList = [] #initialize list of cases, this will be filled with the properly filled case info

    for case in ClientCases:

        print("Downloading case: " + case.case_number + " " + PathToExampleHTMLFiles + case.case_detail_link)

        # set up case parser
        caseparser = CaseParser()

        caseRawData = file2string(PathToExampleHTMLFiles + case.case_detail_link)
        caseparser.feed(caseRawData) #todo: iterator goes here

        ChargeList = [] #initialize empty list of charges

        for charge, contents in caseparser.hashed_charge_data.items(): #iterate through dict of hashed charge data

            if len(caseparser.hashed_dispo_data) > 0: #aparently sometimes there is no dispo data
                ruling = caseparser.hashed_dispo_data[charge]['ruling'] # pull the ruling from the dispo data                   warning: this assumes that the charges and their corresponding dispo data are always indexed in the same order
            else:
                ruling = ''

            newCharge = Charge(contents['name'], contents['statute'], contents['level'], contents['date'], ruling)  #create charge object with the full details

            ChargeList.append(newCharge)

        case.setCharges(ChargeList) #update charge object with completed list of charges from detail parser
        updatedCaseList.append(case)


    return Client(ClientName, ClientDOB, updatedCaseList)


if __name__ == '__main__':
    print("analyzer prototype")

    PathToExampleHTMLFiles = '/home/cameron/PycharmProjects/recordexpungPDX/src/backend/tests/fixtures/html/ward-weaver/'
    client = BuildClientObject(PathToExampleHTMLFiles, WardWeaver.RECORD)
    browse(client)

    PathToExampleHTMLFiles = '/home/cameron/PycharmProjects/recordexpungPDX/src/backend/tests/fixtures/html/bill-sizemore/'
    client = BuildClientObject(PathToExampleHTMLFiles, BillSizemore.RECORD)
    browse(client)


