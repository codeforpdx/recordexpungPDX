"""
This util script generates the user-facing documentation for charge types as an md file.
"""

import pkgutil
from expungeservice.models.charge import Charge
from expungeservice.models.helpers.generator import get_charge_classes


def generate_charge_type_doc():

    manual_doc_string = """# Charge Types
The expungement system defines this custom set of charge types, to compute their correct type eligibility."
"""
    for charge_subclass in get_charge_classes():
        entry_string = f"## {charge_subclass.type_name}\n{charge_subclass.expungement_rules}\n\n"
        manual_doc_string += entry_string
    manual_doc_string += "\n"
    doc_file = open("../../doc/charge_types.md", "w")
    doc_file.write(manual_doc_string[:-2])
    doc_file.close()


generate_charge_type_doc()
