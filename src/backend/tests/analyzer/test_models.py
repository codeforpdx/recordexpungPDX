from expungeservice.models.statute import Statute
import unittest

class TestStatuteModel(unittest.TestCase):

    def setUp(self):
        self.list = ['803455',
                     '483050',
                     '163.175',
                     '811175',
                     '8111751',
                     '806010',
                     '8111751',
                     '806010',
                     '8112101B',
                     '163.375',
                     '163.427',
                     '163.160(2)',
                     '163.095',
                     '163.095',
                     '163.095',
                     '166.085',
                     '163.427',
                     '163.427',
                     '161.405(2)(c)',
                     '163.095',
                     '163.095',
                     '163.095',
                     '166.085',
                     '161.405(2)(a)',
                     '163.375',
                     '163.427',
                     '163.425',
                     '163.415',
                     '163.415',
                     '110151',
                     '811110',
                     '811100',
                     '811100C',
                     '43',
                     '811.100',
                     '43',
                     '43',
                     '811.100',
                     '43',
                     '314.075',
                     '314.075',
                     '314.075']

    def test_chapter_is_3_digit_int_or_None(self):

        for item in self.list:
            newStatute = Statute(item)

            if type(newStatute.chapter) == type(None):
                assert type(newStatute.chapter) == type(None)

            if type(newStatute.subchapter) == type(None):
                assert type(newStatute.subchapter) == type(None)

            if type(newStatute.subchapter) != type(None) and type(newStatute.chapter) != type(None):
                assert len(newStatute.chapter) == 3
                assert len(newStatute.subchapter) == 3


