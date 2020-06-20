from dataclasses import replace, asdict
from datetime import datetime
from typing import List, Tuple, Dict, Any
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
        next_new_case_number = 1
        edited_cases: List[OeciCase] = []
        new_charges_accumulator: List[Charge] = []
        for case in search_result_cases:
            if case.summary.case_number not in edits.keys():
                edited_cases.append(case)
        for edit_action_case_number, edit in edits.items():
            if edit["summary"]["edit_status"] == EditStatus.ADD:
                case = OeciCase.empty(case_number=str(edit["summary"]["case_number"]))
                edited_case, new_charges = RecordEditor._edit_case(case, edit)
                edited_cases.append(edited_case)
                new_charges_accumulator += new_charges
            elif edit["summary"]["edit_status"] == EditStatus.UPDATE:
                for case in search_result_cases:
                    case_number = case.summary.case_number
                    if case_number == edit_action_case_number:
                        edited_case, new_charges = RecordEditor._edit_case(case, edit)
                        edited_cases.append(edited_case)
                        new_charges_accumulator += new_charges
            elif edit["summary"]["edit_status"] == EditStatus.DELETE:
                for case in search_result_cases:
                    case_number = case.summary.case_number
                    if case.summary.case_number == edit_action_case_number:
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
            else:
                case_summary_edits[key] = value
        edited_summary = replace(case.summary, **case_summary_edits)
        new_charges: List[Charge] = []
        if case_summary_edits["edit_status"] == EditStatus.DELETE:
            edited_charges = RecordEditor._mark_charges_as_deleted(case.charges,)
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

        charges_without_charge_type, charges_with_charge_type = RecordEditor._update_and_delete_charges(
            case_number, charges, charges_edits
        )
        charges_with_charge_type += RecordEditor._add_charges(case_number, charges, charges_edits)
        return tuple(charges_without_charge_type), charges_with_charge_type

    @staticmethod
    def _update_and_delete_charges(
        case_number: str, charges: Tuple[OeciCharge, ...], charges_edits: Dict[str, Dict[str, str]]
    ) -> Tuple[List[OeciCharge], List[Charge]]:
        # Deleting a charge does nothing except set its edit_status to DELETED,
        # so it is performed by just updating that field.
        charges_without_charge_type, charges_with_charge_type = [], []
        for charge in charges:
            if charge.ambiguous_charge_id in charges_edits.keys():
                charge_edits = charges_edits[charge.ambiguous_charge_id]
                charge_dict = RecordEditor._parse_charge_edits(charge_edits)
                if charge_dict.get("edit_status", None) != EditStatus.DELETE:
                    charge_dict["edit_status"] = EditStatus.UPDATE
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
                    charges_with_charge_type.append(new_charge)
                else:
                    charges_without_charge_type.append(edited_oeci_charge)
            else:
                charges_without_charge_type.append(charge)
        return charges_without_charge_type, charges_with_charge_type

    @staticmethod
    def _add_charges(
        case_number, charges: Tuple[OeciCharge, ...], charges_edits: Dict[str, Dict[str, str]]
    ) -> List[Charge]:
        new_charges = []
        for ambiguous_charge_id, charge_edits in charges_edits.items():
            charge_ids = [charge.ambiguous_charge_id for charge in charges]
            if ambiguous_charge_id not in charge_ids:
                charge_dict = RecordEditor._parse_charge_edits(charge_edits)
                charge_type_string = charge_dict.pop("charge_type", None)
                charge_edits_with_defaults = {
                    **charge_dict,
                    "charge_type": RecordEditor._get_charge_type(charge_type_string),
                    "ambiguous_charge_id": ambiguous_charge_id,
                    "case_number": case_number,
                    "id": f"{ambiguous_charge_id}-0",
                    "name": "N/A",
                    "statute": "N/A",
                    "level": "N/A",
                    "type_name": "N/A",
                    "balance_due_in_cents": 0,
                    "edit_status": EditStatus.ADD,
                }
                new_charge = from_dict(data_class=Charge, data=charge_edits_with_defaults)
                new_charges.append(new_charge)
        return new_charges

    @staticmethod
    def _get_charge_type(charge_type: str) -> ChargeType:
        charge_types = get_charge_classes()
        charge_types_dict = {charge_type.__name__: charge_type() for charge_type in charge_types}
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
