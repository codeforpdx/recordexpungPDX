import unittest
import flask
import json

from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.expunger import Expunger
from expungeservice.models.disposition import Disposition
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.record_factory import RecordFactory

from expungeservice.serializer import ExpungeModelJsonifier


case = CaseFactory.create()
mrd_charge = ChargeFactory.create_dismissed_charge()
case.charges = [mrd_charge]

record = Record([case])
print(type(record))

print(json.dumps(record, cls = ExpungeModelJsonifier, indent = 4))