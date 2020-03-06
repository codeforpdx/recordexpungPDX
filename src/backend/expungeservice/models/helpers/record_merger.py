from typing import List, Dict, Set

from expungeservice.models.ambiguous import AmbiguousRecord
from expungeservice.models.expungement_result import TimeEligibility
from expungeservice.models.record import Record
import collections


class RecordMerger:
    @staticmethod
    def merge(
        ambiguous_record: AmbiguousRecord, charge_id_to_time_eligibility_list: List[Dict[str, TimeEligibility]]
    ) -> Record:
        charge_id_to_time_eligibilities: Dict[str, Set[TimeEligibility]] = collections.defaultdict(set)
        for charge_id_to_time_eligibility in charge_id_to_time_eligibility_list:
            for k, v in charge_id_to_time_eligibility.items():
                charge_id_to_time_eligibilities[k].add(v)
        record = ambiguous_record[0]
        for charge in record.charges:
            charge.expungement_result.time_eligibility = RecordMerger.merge_time_eligibilities(
                charge_id_to_time_eligibilities[charge.id]
            )
        return record

    @staticmethod
    def merge_time_eligibilities(time_eligibilities: Set[TimeEligibility]):
        return (
            time_eligibilities.pop()
        )  # TODO: Fix stub which assumes set is always of size 1 and actually do a meaningful merge.
