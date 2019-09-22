
import unittest.mock

print("\nimportthing the thing module in the dump testing file\n")
from tests import thing_module

mocker = unittest.mock.Mock()


print("top of testing file, about to usng calling_a_thing()")
thing_module.calling_a_thing()


class FakeGiver():
    def give_stuff(self):
        return "fake stuff from fake giver"

class TestTheThing(unittest.TestCase):

    @unittest.mock.patch("tests.thing_module.Thing")
    def test_a_caller_of_a_thing(self, mock):

        #mock.return_value = FakeGiver()
        mock.return_value.give_stuff.return_value = "fake stuff" #FakeGiver()


        print("calling_a_thing in the test case")
        thing_module.calling_a_thing()

