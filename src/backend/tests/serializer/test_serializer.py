from expungeservice.serializer import ExpungeModelEncoder
from tests.factories.crawler_factory import CrawlerFactory

import unittest
import json

class TestRecordObjectSerializer(unittest.TestCase):

    def test_it_creates_json(self):

        crawler = CrawlerFactory.setup()
        record = CrawlerFactory.create(crawler)

        jsonified_dictionary = json.loads(json.dumps(record, cls=ExpungeModelEncoder))
        assert type(jsonified_dictionary) == dict