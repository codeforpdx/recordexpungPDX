import unittest

from tests.fixtures.post_login_page import PostLoginPage
from expungeservice.crawler.parsers.node_parser import NodeParser


class TestNodeParser(unittest.TestCase):

    def test_payload(self):
        self.parser = NodeParser()
        self.parser.feed(PostLoginPage.POST_LOGIN_PAGE)
        response_node_ids = '101100,102100,103100'
        assert self.parser.node_id == response_node_ids
