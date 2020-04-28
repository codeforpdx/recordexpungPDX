import re
from typing import Tuple, Optional

from dacite import from_dict

from expungeservice.models.ambiguous import AmbiguousCharge
from expungeservice.charge_classifier import ChargeClassifier
from expungeservice.models.record import Question


class ChargeCreator:
    @staticmethod
    def create(charge_id, **kwargs) -> Tuple[AmbiguousCharge, Optional[Question]]:
        case_number = kwargs["case_number"]
        violation_type = kwargs["violation_type"]
        name = kwargs["name"]
        statute = ChargeCreator.__strip_non_alphanumeric_chars(kwargs["statute"])
        level = kwargs["level"]
        section = ChargeCreator.__set_section(statute)
        birth_year = kwargs.get("birth_year")
        disposition = kwargs.get("disposition")
        ambiguous_charge_type_with_questions = ChargeClassifier(
            violation_type, name, statute, level, section, birth_year, disposition
        ).classify()
        kwargs["_section"] = section
        kwargs["statute"] = statute
        kwargs["ambiguous_charge_id"] = f"{case_number}-{charge_id}"
        classifications = ambiguous_charge_type_with_questions.ambiguous_charge_type
        question = ambiguous_charge_type_with_questions.question
        options = ambiguous_charge_type_with_questions.options
        assert len(classifications) == len(options) if options else True
        ambiguous_charge = []
        options_dict = {}
        for i, classification in enumerate(classifications):
            uid = f"{case_number}-{charge_id}-{i}"
            charge_dict = {**kwargs, "id": uid}
            charge = from_dict(data_class=classification, data=charge_dict)
            ambiguous_charge.append(charge)
            if options:
                options_dict[options[i]] = uid
        if question:
            ambiguous_charge_id = ambiguous_charge[0].ambiguous_charge_id
            return ambiguous_charge, Question(ambiguous_charge_id, case_number, question, options_dict)
        else:
            return ambiguous_charge, None

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r"[^a-zA-Z0-9*]", "", statute).upper()

    @staticmethod
    def __set_section(statute):
        if len(statute) < 6:
            return ""
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
