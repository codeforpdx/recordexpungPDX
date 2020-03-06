from typing import List, Dict

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.models.expungement_result import TimeEligibility
from expungeservice.models.record import Record


class RecordMerger:
    @staticmethod
    def merge(
        ambiguous_record: AmbiguousRecord, charge_id_to_time_eligibilities: List[Dict[str, TimeEligibility]]
    ) -> Record:
        return ambiguous_record[0]
