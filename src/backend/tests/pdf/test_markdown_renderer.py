import json

import pytest

from expungeservice.pdf.markdown_renderer import MarkdownRenderer
from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.serializer import ExpungeModelEncoder
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe

@pytest.fixture
def example_record():
    return CrawlerFactory.create(
        record=JohnDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_WITH_REVOKED_PROBATION,
        },
    )


def test_render_markdown(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    aliases = [
        {"first_name": "john", "middle_name": "", "last_name": "smith", "birth_date": "2/2/2020"},
        {"first_name": "john", "middle_name": "", "last_name": "doe", "birth_date": ""},
    ]
    header = MarkdownSerializer.default_header(aliases)
    source = MarkdownRenderer.to_markdown(record, header)
    assert source == open("./tests/pdf/expected_markdown.md").read()
