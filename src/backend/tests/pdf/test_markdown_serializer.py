import json

import pytest

from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.serializer import ExpungeModelEncoder
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe

EXPECTED_MARKDOWN = """# EXPUNGEMENT ANALYSIS REPORT  
## Search Terms  
Name: JOHN  SMITH DOB: 2/2/2020  
Name: JOHN  DOE  
  
  
## Charges Eligible Now  
 - Possession of Cocaine (DISMISSED) - Arrested Feb 17, 2009 - $ owed  
  
  
## Future Eligible Charges  
The following charges (dismissed and convicted) are eligible at the designated dates.  
### Eligible Nov 9, 2020  
 - Possession of Cocaine (CONVICTED) - Arrested Jun 13, 2009 - $ owed  

  
"""


@pytest.fixture
def example_record():
    return CrawlerFactory.create(
        record=JohnDoe.SINGLE_CASE_RECORD, cases={"CASEJD1": CaseDetails.CASE_WITH_REVOKED_PROBATION,},
    )


def test_pdf_print(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    aliases = [
        {"first_name": "john", "middle_name": "", "last_name": "smith", "birth_date": "2/2/2020"},
        {"first_name": "john", "middle_name": "", "last_name": "doe", "birth_date": ""},
    ]
    header = MarkdownSerializer.default_header(aliases)
    source = MarkdownSerializer.to_markdown(record, header)
    assert source == EXPECTED_MARKDOWN
