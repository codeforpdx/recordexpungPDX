import unittest
from ..fixtures.search_page_response import SearchPageResponse
from expungeservice.crawler.parsers.param_parser import ParamParser


class TestParamParser(unittest.TestCase):
    def setUp(self):
        self.parser = ParamParser()
        self.parser.feed(SearchPageResponse.RESPONSE)

    def test_it_parses_event_target(self):
        assert self.parser.event_target == "bleh"

    def test_it_parses_event_argument(self):
        assert self.parser.event_argument == "boo"

    def test_it_parses_view_state(self):
        assert self.parser.view_state == "billy bob"

    def test_it_parses_view_state_generator(self):
        assert self.parser.view_state_generator == "thornton"

    def test_it_parses_event_validation(self):
        assert self.parser.event_validation == "validate"

    def test_it_parses_node_id(self):
        assert self.parser.node_id == "a lot of nodes"
