import unittest

from expungeservice.RapSheetAnalyzer.analyze import *
from expungeservice.RapSheetAnalyzer.ineligible_crimes_list import *


class TestIneligibleListSearcher(unittest.TestCase):

"""

This script should take data from the parser and turn it into a client rapsheet object

"""

#todo: delete this file

#todo: make this conform to formatting standards of the project


from tests.fixtures.john_doe import JohnDoe # this is the pre downloaded john doe record in HTML format
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.RapSheetAnalyzer.analyze import *

parser = RecordParser()  #initialize the record parser
parser.feed(JohnDoe.RECORD)  #Feed our example rap sheet into the parser (client name john doe)



#   ***********
#   *********** create our client
#   ***********

# step 1:
# we take our clients info from the first case on the rap sheet
# #todo: this logic seems sketchy
# #todo: maybe verify that all cases are from the client name


ClientName = parser.cases[0].name
ClientDOB = parser.cases[0].birth_year #todo: refactor "birth_year"

#step 2:
# use parsed case data to create case objects

for case in parser.cases:

    print('###' + case.case_number)
    print('###' + case.current_status)
    print('###' + case.violation_type)

    for charge in case.charges:
        print(charge)

        #newCharge = Charge(charge, )




#ourClient = Client(ClientName, ClientDOB, ClientCases)






