import unittest
from expungeservice.expunger.helper_functions import *

from expungeservice.expunger.analyze import *
from expungeservice.expunger.client_builder import *

from tests.fixtures.bill_sizemore import BillSizemore
from tests.fixtures.ward_weaver import WardWeaver

import tests.fixtures.bill_sizemore as bill

import os

import logging

logging.basicConfig(level=logging.CRITICAL)


class TestAnalyzerWithBillSizemorerCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(bill.__file__)
        path = path.replace(os.path.relpath(path, "../../"), "")
        PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/bill-sizemore') + "/"

        self.client = BuildClientObject(PathToExampleHTMLFiles, BillSizemore.RECORD)

        #print(self.client.toJSON())

        self.analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object
        self.analyzer.analyze()

        #browse(self.client)

        # #was using object browser for object inspection but now
        # using json output since this program is going into a docker container
        # but the object browser is pretty cool

    def test_name(self):
        assert self.client.name == "SIZEMORE, WILLIAM"

    def test_DOB_is_datetime_obj(self):
        assert type(self.client.dob) == type(datetime.today().date())

    def test_DOB(self):
        assert self.client.dob.__str__() == "1951-06-02"

    def test_first_case(self):

        print(OBJtoJSON(self.client.cases[0].charges[0])) #prints this charge object to terminal for manual inspection

        assert self.client.cases[0].charges[0].eligible_when == "never"

    def test_second_case(self):
        assert self.client.cases[1].charges[0].eligible_when == "never"

class TestAnalyzerWithWardWeaverCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(bill.__file__)
        path = path.replace(os.path.relpath(path, "../../"), "")
        PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/ward-weaver') + "/"

        self.client = BuildClientObject(PathToExampleHTMLFiles, WardWeaver.RECORD)  # use parser to build complete client object                                                                                                      # use object browser to visually inspect completeness of object

        self.analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object
        self.analyzer.analyze()

    def test_name(self):
        assert self.client.name == "WEAVER, WARD FRANCIS, III"

    def test_DOB_is_datetime_obj(self):
        assert type(self.client.dob) == type(datetime.today().date())

