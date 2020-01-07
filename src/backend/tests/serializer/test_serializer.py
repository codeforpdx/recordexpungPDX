import pytest

from expungeservice.expunger.expunger import Expunger
from expungeservice.serializer import ExpungeModelEncoder

import json

from tests.functional_tests.test_crawler_expunger import (
    record_with_open_case,
    empty_record,
    partial_dispos_record,
    record_without_dispos,
    record_with_various_categories,
    record_with_specific_dates,
    crawler,
)


@pytest.fixture(
    params=[
        pytest.lazy_fixture("record_with_open_case"),
        pytest.lazy_fixture("empty_record"),
        pytest.lazy_fixture("partial_dispos_record"),
        pytest.lazy_fixture("record_without_dispos"),
        pytest.lazy_fixture("record_with_various_categories"),
        pytest.lazy_fixture("record_with_specific_dates"),
    ]
)
def _record(request):
    return request.param


def test_round_trip_various_records(_record):
    expunger = Expunger(_record)
    expunger.run()
    json.loads(json.dumps(_record, cls=ExpungeModelEncoder))
