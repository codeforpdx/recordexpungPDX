from dataclasses import replace, asdict
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
from expungeservice.util import DateWithFuture as date_class

from dacite import from_dict

from expungeservice.generator import get_charge_classes
from expungeservice.models.charge import Charge, OeciCharge, ChargeType, EditStatus
from expungeservice.models.case import OeciCase, CaseCreator
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.disposition import DispositionCreator


class RecordEditor:
    @staticmethod
    def edit_search_results(search_result_cases: List[OeciCase], edits) -> Tuple[List[OeciCase], List[Charge]]:
        edited_cases: List[OeciCase] = []
        new_charges_accumulator: List[Charge] = []
        for case in search_result_cases:
            if case.summary.case_number not in edits.keys():
                edited_cases.append(case)
        for edit_action_case_number, edit in edits.items():
            if edit["summary"]["edit_status"] == EditStatus.ADD:
                case = OeciCase.empty(case_number=str(edit["summary"]["case_number"]))
            elif edit["summary"]["edit_status"] in (EditStatus.UPDATE, EditStatus.DELETE, EditStatus.UNCHANGED):
                case = next(
                    (case for case in search_result_cases if case.summary.case_number == edit_action_case_number)
                )
            else:
                raise ValueError(f"Unknown edit status for case {case.summary.case_number}")
            edited_case, new_charges = RecordEditor._edit_case(case, edit)
            edited_cases.append(edited_case)
            new_charges_accumulator += new_charges
        return edited_cases, new_charges_accumulator

    @staticmethod
    def _edit_case(case: OeciCase, case_edits) -> Tuple[OeciCase, List[Charge]]:
        case_summary_edits: Dict[str, Any] = {}
        for key, value in case_edits["summary"].items():
            if key == "edit_status":
                case_summary_edits["edit_status"] = EditStatus(value)
            if key == "date":
                case_summary_edits["date"] = date_class.fromdatetime(datetime.strptime(value, "%m/%d/%Y"))
            elif key == "balance_due":
                case_summary_edits["balance_due_in_cents"] = CaseCreator.compute_balance_due_in_cents(value)
            elif key == "birth_year":
                case_summary_edits["birth_year"] = int(value)
            elif key == "restitution":
                case_summary_edits["restitution"] = value == "True"
            else:
                case_summary_edits[key] = value
        edited_summary = replace(case.summary, **case_summary_edits)
        new_charges: List[Charge] = []
        if case_summary_edits["edit_status"] == EditStatus.DELETE:
            edited_charges = RecordEditor._mark_charges_as_deleted(case.charges)
        elif "charges" in case_edits.keys():
            edited_charges, new_charges = RecordEditor._edit_charges(
                case.summary.case_number, case.charges, case_edits["charges"]
            )
        else:
            edited_charges = case.charges
        return OeciCase(edited_summary, edited_charges), new_charges

    @staticmethod
    def _mark_charges_as_deleted(charges: Tuple[OeciCharge, ...]) -> Tuple[OeciCharge, ...]:
        deleted_charges = []
        for charge in charges:
            deleted_charge = replace(charge, edit_status=EditStatus.DELETE)
            deleted_charges.append(deleted_charge)
        return tuple(deleted_charges)

    @staticmethod
    def _edit_charges(
        case_number: str, charges: Tuple[OeciCharge, ...], charges_edits: Dict[str, Dict[str, str]]
    ) -> Tuple[Tuple[OeciCharge, ...], List[Charge]]:
        charges_without_charge_type = [
            charge for charge in charges if charge.ambiguous_charge_id not in charges_edits.keys()
        ]
        charges_with_charge_type = []
        for edit_action_ambiguous_charge_id, edit in charges_edits.items():
            if edit.get("edit_status", None) == EditStatus.ADD:
                new_charge = RecordEditor._add_charge(case_number, edit_action_ambiguous_charge_id, edit)
                charges_with_charge_type.append(new_charge)
            else:  # edit["edit_status"] is either UPDATE or DELETE
                updated_charge = RecordEditor._update_or_delete_charge(
                    charges, case_number, edit_action_ambiguous_charge_id, edit
                )
                if isinstance(updated_charge, Charge):
                    charges_with_charge_type.append(updated_charge)
                else:
                    charges_without_charge_type.append(updated_charge)
        return tuple(charges_without_charge_type), charges_with_charge_type

    @staticmethod
    def _add_charge(case_number, ambiguous_charge_id, edit) -> Charge:
        charge_dict = RecordEditor._parse_charge_edits(edit)
        charge_type = RecordEditor._get_charge_type(charge_dict.pop("charge_type", None))
        charge_edits_with_defaults = {
            "name": "",
            **charge_dict,
            "charge_type": charge_type,
            "ambiguous_charge_id": ambiguous_charge_id,
            "case_number": case_number,
            "id": f"{ambiguous_charge_id}-0",
            "statute": "",
            "type_name": charge_type.type_name,
            "balance_due_in_cents": 0,
            "edit_status": EditStatus.ADD,
        }
        return from_dict(data_class=Charge, data=charge_edits_with_defaults)

    @staticmethod
    def _update_or_delete_charge(charges, case_number, edit_action_ambiguous_charge_id, edit) -> OeciCharge:
        charge = next((charge for charge in charges if charge.ambiguous_charge_id == edit_action_ambiguous_charge_id))
        charge_dict = RecordEditor._parse_charge_edits(edit)
        charge_type_string = charge_dict.pop("charge_type", None)
        edited_oeci_charge = replace(charge, **charge_dict)
        if charge_type_string:
            charge_type_data = {
                "id": f"{charge.ambiguous_charge_id}-0",
                "case_number": case_number,
                "charge_type": RecordEditor._get_charge_type(charge_type_string),
                **asdict(edited_oeci_charge),
            }
            new_charge = from_dict(data_class=Charge, data=charge_type_data)
            return new_charge
        else:
            return edited_oeci_charge

    @staticmethod
    def _get_charge_type(charge_type: str) -> ChargeType:
        charge_types = get_charge_classes()
        charge_types_dict = {
            **{charge_type.__name__: charge_type() for charge_type in charge_types},
            **{charge_type.type_name: charge_type() for charge_type in charge_types},
        }
        return charge_types_dict.get(charge_type, UnclassifiedCharge())

    @staticmethod
    def _parse_charge_edits(charge_edits):
        charge_dict: Dict[str, Any] = {}
        for key, value in charge_edits.items():
            if key == "disposition":
                disposition = value
                if disposition:
                    charge_dict["disposition"] = DispositionCreator.create(
                        date_class.fromdatetime(datetime.strptime(disposition["date"], "%m/%d/%Y")),
                        disposition["ruling"],
                    )
                else:
                    charge_dict["disposition"] = None
            elif key in ("date", "probation_revoked"):
                if value:
                    charge_dict[key] = date_class.fromdatetime(datetime.strptime(value, "%m/%d/%Y"))
            elif key == "edit_status":
                charge_dict[key] = EditStatus(value)
            else:
                charge_dict[key] = value
        return charge_dict
