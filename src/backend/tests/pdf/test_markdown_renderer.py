import json

import pytest

from expungeservice.pdf.markdown_renderer import MarkdownRenderer
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
  
## PLEASE READ THIS 

### Disclaimer:
RecordSponge is not your lawyer. The results below should be used as a guide only. If you are relying on this information to expunge your record, please email roe@qiu-qiulaw.com for free consultation.  \n



### Assumptions
<b>1) Successful completion of court requirements</b> &nbsp; If you are currently on probation or conditional discharge, the analysis below assumes that you will successfully complete those requirements.  \n
<b>2) Court debt paid off</b> &nbsp; You must pay off all court debt on a case before you file for expungement on any case which you are otherwise eligible to expunge.  \n
<b>3) No records outside of Oregon State court from last seven years</b> &nbsp; We are only able to access your public Oregon records. Your analysis may be different if you have had cases from <b>within the last seven years</b> which were:  \n
  * from States besides Oregon
  * from Federal Court (in any State)
  * from local District Courts, e.g. Medford Municipal Court (not Jackson Circuit Court)
  * already expunged 

Below is a summary of your eligibility for expungement based on the assumptions above. 
If the above assumptions are not true for you and you would like an updated analysis, email roe@qiu-qiulaw.com with your name and date of birth with subject line, “Updated Analysis”.  
## Charges Eligible Now  
You are not currently eligible to expunge any charges.  
  
  
## Charges Eligible Now If Balance Paid  
These convictions are eligible as soon as the balance of fines on the case is paid.  

 - Multnomah CASEJD1 – $529.08 
     - Possession of Cocaine (CONVICTED) Charged Jun 13, 2009 
     - Possession of Cocaine (DISMISSED) Charged Feb 17, 2009 
  
 
  
"""


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
    print(source)
    assert source == EXPECTED_MARKDOWN
