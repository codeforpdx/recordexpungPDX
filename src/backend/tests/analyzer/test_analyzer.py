

import unittest
from expungeservice.expunger.helper_functions import *

from expungeservice.expunger.analyze import *
from expungeservice.expunger.client_builder import *

from tests.fixtures.jd_litters import Litter
from tests.fixtures.jd_taxes import Taxes
from tests.fixtures.jd_murders import Murder

import tests.fixtures.jd_litters as jd_litters
import os
import logging
logging.basicConfig(level=logging.INFO)

from objbrowser import browse


#todo: freeze the client objects so these tests dont depend on the parser

class TestAnalyzerWithJdLitter(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(jd_litters.__file__)
        path = path.replace(os.path.relpath(path, "../../"), "")
        PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/jd-litter') + "/"

        self.client = BuildClientObject(PathToExampleHTMLFiles, Litter.RECORD)

        self.analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object

        browse(self.client)


    def test_name(self):
        assert self.client.name == "litter, john doe"

    def test_DOB_is_datetime_obj(self):
        assert type(self.client.dob) == type(datetime.today().date())

    def test_DOB(self):
        assert self.client.dob.__str__() == "1969-04-20"

    # def test_first_case(self):
    #
    #     assert self.client.cases[0].charges[0].eligible_when == "never"
    #
    # def test_second_case(self):
    #     assert self.client.cases[1].charges[0].eligible_when == "never"

#
# class TestAnalyzerWithjJD-Taxes(unittest.TestCase):
#
#     def setUp(self):
#         path = os.path.abspath(bill.__file__)
#         path = path.replace(os.path.relpath(path, "../../"), "")
#         PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/bill-sizemore') + "/"
#
#         self.client = BuildClientObject(PathToExampleHTMLFiles, BillSizemore.RECORD)
#
#         self.analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object
#
#         browse(self.client)
#
#     def test_name(self):
#         assert self.client.name == "SIZEMORE, WILLIAM"
#
#     def test_DOB_is_datetime_obj(self):
#         assert type(self.client.dob) == type(datetime.today().date())
#
#     def test_DOB(self):
#         assert self.client.dob.__str__() == "1951-06-02"
#
#     def test_first_case(self):
#
#         assert self.client.cases[0].charges[0].eligible_when == "never"
#
#     def test_second_case(self):
#         assert self.client.cases[1].charges[0].eligible_when == "never"
#
# class TestAnalyzerWithJDMurdersCase(unittest.TestCase):
#
#     def setUp(self):
#         path = os.path.abspath(ass.__file__)
#         path = path.replace(os.path.relpath(path, "../../"), "")
#         PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/cameron-litters') + "/"
#
#         self.client = BuildClientObject(PathToExampleHTMLFiles, Murder.RECORD)  # use parser to build complete client object
#         self.analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object
#
#         browse(self.client)
#
#     def test_name(self):
#         assert self.client.name == "WEAVER, WARD FRANCIS, III"
#
#     def test_DOB_is_datetime_obj(self):
#         assert type(self.client.dob) == type(datetime.today().date())

