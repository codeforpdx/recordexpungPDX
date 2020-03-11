import json

from hypothesis import given, settings, HealthCheck

from expungeservice.expunger import Expunger
from expungeservice.models.helpers.generator import build_record_strategy
from expungeservice.models.helpers.record_merger import RecordMerger
from expungeservice.serializer import ExpungeModelEncoder


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(build_record_strategy())
def test_round_trip_various_records(record):
    expunger = Expunger(record)
    expunger_result = expunger.run()
    updated_record = RecordMerger.merge([record], [expunger_result])
    json.loads(json.dumps(updated_record, cls=ExpungeModelEncoder))
