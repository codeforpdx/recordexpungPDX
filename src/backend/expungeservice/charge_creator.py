import re
from typing import Tuple, Optional

from dacite import from_dict

from expungeservice.models.ambiguous import AmbiguousCharge
from expungeservice.charge_classifier import ChargeClassifier
from expungeservice.models.charge import Charge
from expungeservice.models.record import Question


class ChargeCreator:
    @staticmethod
    def create(ambiguous_charge_id, **kwargs) -> Tuple[AmbiguousCharge, Optional[Question]]:
        violation_type = kwargs["violation_type"]
        name = kwargs["name"]
        level = kwargs["level"]
        statute = ChargeCreator._strip_non_alphanumeric_chars(kwargs["statute"])
        section = ChargeCreator._set_section(statute)
        birth_year = kwargs.get("birth_year")
        disposition = kwargs["disposition"]
        location = kwargs["location"]
        ambiguous_charge_type_with_questions = ChargeClassifier(
            violation_type, name, statute, level, section, birth_year, disposition, location
        ).classify()
        kwargs["statute"] = statute
        kwargs["ambiguous_charge_id"] = ambiguous_charge_id
        classifications = ambiguous_charge_type_with_questions.ambiguous_charge_type
        question = ambiguous_charge_type_with_questions.question
        ambiguous_charge = []
        for i, classification in enumerate(classifications):
            uid = f"{ambiguous_charge_id}-{i}"
            charge_dict = {**kwargs, "id": uid, "charge_type": classification}
            charge = from_dict(data_class=Charge, data=charge_dict)
            ambiguous_charge.append(charge)
        if question:
            return ambiguous_charge, question
        else:
            return ambiguous_charge, None

    @staticmethod
    def _strip_non_alphanumeric_chars(statute):
        return re.sub(r"[^a-zA-Z0-9*]", "", statute).upper()

    @staticmethod
    def _set_section(statute):
        if len(statute) < 6:
            return ""
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
