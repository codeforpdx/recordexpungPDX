"""
This util script generates the user-facing documentation for charge types as an md file.
"""

import sys
from os import getcwd
sys.path.append(getcwd())
from expungeservice.models.charge import Charge
from expungeservice.models.helpers.generator import get_charge_classes


def generate_charge_type_doc():
    manual_doc_string = """# Charge Types
The expungement system defines this custom set of charge types, to compute their correct type eligibility."
"""
    for charge_subclass in get_charge_classes():
        entry_string = "## {0}\n{1}\n\n".format(charge_subclass.type_name, charge_subclass.expungement_rules)
        manual_doc_string += entry_string
    manual_doc_string += "\n"
    doc_file = open("../../doc/charge_types.md", "w")
    doc_file.write(manual_doc_string[:-2])
    doc_file.close()


if __name__ == '__main__':
    generate_charge_type_doc()
