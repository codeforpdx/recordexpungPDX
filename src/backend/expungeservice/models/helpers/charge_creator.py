import re
from datetime import datetime
from dacite import from_dict

from expungeservice.models.ambiguous import AmbiguousCharge
from expungeservice.models.helpers.charge_classifier import ChargeClassifier


class ChargeCreator:
    @staticmethod
    def create(charge_id, **kwargs) -> AmbiguousCharge:
        case_number = kwargs["case_number"]
        violation_type = kwargs["violation_type"]
        name = kwargs["name"]
        statute = ChargeCreator.__strip_non_alphanumeric_chars(kwargs["statute"])
        level = kwargs["level"]
        chapter = ChargeCreator._set_chapter(kwargs["statute"])
        section = ChargeCreator.__set_section(statute)
        disposition = kwargs.get("disposition")
        classifications = ChargeClassifier(
            violation_type, name, statute, level, chapter, section, disposition
        ).classify()
        kwargs["date"] = datetime.date(datetime.strptime(kwargs["date"], "%m/%d/%Y"))
        kwargs["_chapter"] = chapter
        kwargs["_section"] = section
        kwargs["statute"] = statute
        kwargs["ambiguous_charge_id"] = f"{case_number}-{charge_id}"
        ambiguous_charge = []
        for i, classification in enumerate(classifications):
            uid = f"{case_number}-{charge_id}-{i}"
            charge_dict = {**kwargs, "id": uid}
            charge = from_dict(data_class=classification, data=charge_dict)
            ambiguous_charge.append(charge)
        return ambiguous_charge

    @staticmethod
    def __strip_non_alphanumeric_chars(statute):
        return re.sub(r"[^a-zA-Z0-9*]", "", statute).upper()

    @staticmethod
    def _set_chapter(statute):
        if "." in statute:
            return statute.split(".")[0]
        else:
            return None

    @staticmethod
    def __set_section(statute):
        if len(statute) < 6:
            return ""
        elif statute[3].isalpha():
            return statute[0:7]
        return statute[0:6]
