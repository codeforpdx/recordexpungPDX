import unittest

from expungeservice.expunger.analyze import *
from expungeservice.expunger.client_builder import *

import tests.fixtures.bill_sizemore as bill

import os


class TestAnalyzerWithBillSizemorerCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(bill.__file__)
        path = path.replace(os.path.relpath(path, "../../"), "")
        PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/bill-sizemore') + "/"

        self.client = BuildClientObject(PathToExampleHTMLFiles, BillSizemore.RECORD)

        analyzer = RecordAnalyzer(self.client)  # create an analyzer object with our client object
        analyzer.analyze()

    def test_name(self):
        assert self.client.name == "SIZEMORE, WILLIAM"

    def test_DOB_is_datetime_obj(self):
        assert type(self.client.dob) == type(datetime.today().date())



class TestAnalyzerWithWardWeaverCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(bill.__file__)
        path = path.replace(os.path.relpath(path, "../../"), "")
        PathToExampleHTMLFiles = os.path.join(path, 'tests/fixtures/html/ward-weaver') + "/"

        client = BuildClientObject(PathToExampleHTMLFiles, WardWeaver.RECORD)  # use parser to build complete client object                                                                                                      # use object browser to visually inspect completeness of object

        analyzer = RecordAnalyzer(client)  # create an analyzer object with our client object
        analyzer.analyze()

        def test_name(self):
            assert self.client.name == "WEAVER, WARD FRANCIS, III"

        def test_DOB_is_datetime_obj(self):
            assert type(self.client.dob) == type(datetime.today().date())

