import json

import pytest

from expungeservice.pdf.markdown_renderer import MarkdownRenderer
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
    
"""def test_render_markdown(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    aliases = [
        {"first_name": "john", "middle_name": "", "last_name": "smith", "birth_date": "2/2/2020"},
        {"first_name": "john", "middle_name": "", "last_name": "doe", "birth_date": ""},
    ]
    source = MarkdownRenderer.to_markdown(record, aliases=aliases)
    assert source == open("./tests/pdf/expected/default.md").read()"""

def test_render_with_custom_header(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    header = "# Custom Header"
    source = MarkdownRenderer.to_markdown(record, header=header)
    assert source == open("./tests/pdf/expected/custom_header.md").read()
