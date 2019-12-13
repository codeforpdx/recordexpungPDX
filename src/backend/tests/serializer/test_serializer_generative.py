import json

from hypothesis import given

from expungeservice.expunger.expunger import Expunger
from expungeservice.models.helpers.generator import build_record_strategy
from expungeservice.serializer import ExpungeModelEncoder

@given(build_record_strategy())
def test_round_trip_various_records(record):
    expunger = Expunger(record)
    expunger.run()
    json.loads(json.dumps(record, cls=ExpungeModelEncoder))
