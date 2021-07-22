import React from "react";
import Eligibility from "./Eligibility";
import TimeEligibility from "./TimeEligibility";
import TypeEligibility from "./TypeEligibility";
import EditChargePanel from "./EditChargePanel";
import ExpungementRules from "./ExpungementRules";
import EditButton from "./EditButton";
import EditedBadge from "./EditedBadge";
import Questions from "./Questions";
import { ChargeData } from "./types";
import { undoEditCharge } from "../../../redux/search/actions";
import store from "../../../redux/store";

interface Props {
  charge: ChargeData;
  editing: boolean;
  isNewCharge: boolean;
  showEditButtons: boolean;
  whenEditing: Function;
  whenDoneEditing: Function;
}
interface State {
  editing: Boolean;
}
export default class Charge extends React.Component<Props, State> {
  state: State = {
    editing: this.props.editing,
  };

  handleUndoEditClick = () => {
    if (
      !(this.props.charge.edit_status === "ADD") ||
      window.confirm("This data will be lost. Remove anyway?")
    ) {
      store.dispatch(
        undoEditCharge(
          this.props.charge.case_number,
          this.props.charge.ambiguous_charge_id
        )
      );
    }
  };

  render() {
    const {
      edit_status,
      ambiguous_charge_id,
      date,
      disposition,
      statute,
      name,
      type_name,
      level,
      expungement_result,
      expungement_rules,
    } = this.props.charge;

    const dispositionEvent = (disposition: any) => {
      let dispositionEvent;
      dispositionEvent = disposition.status;
      if (
        disposition.status === "Convicted" ||
        disposition.status === "Dismissed"
      ) {
        dispositionEvent += " - " + disposition.date;
      } else if (disposition.status === "Unrecognized") {
        dispositionEvent += ' ("' + disposition.ruling + '")';
      } else if (disposition.status === "Unknown") {
        dispositionEvent = "Unknown";
      }
      if (disposition.amended) {
        dispositionEvent += " (Amended)";
      }
      return dispositionEvent;
    };

    const buildDisposition = (disposition: any) => {
      return (
        <li className="flex mb2">
          <span className="w6rem shrink-none fw7">Disposition</span>{" "}
          {dispositionEvent(disposition)}
        </li>
      );
    };

    const buildRecordTime = () => {
      if (
        (expungement_result.type_eligibility.status === "Eligible" ||
          expungement_result.type_eligibility.status ===
            "Needs More Analysis") &&
        expungement_result.time_eligibility
      ) {
        return (
          <TimeEligibility
            time_eligibility={expungement_result.time_eligibility}
          />
        );
      }
    };

    return (
      <div className="relative br3 bg-white ma2" id={ambiguous_charge_id}>
        {this.props.isNewCharge ? null : (
          <>
            {edit_status !== "DELETE" && (
              <div className="relative connect connect-result pr6">
                <Eligibility
                  expungement_result={expungement_result}
                  removed={edit_status === "DELETE"}
                />
              </div>
            )}
            {edit_status !== "UNCHANGED" && (
              <div className="absolute top-2 right-0 ph1 pv1">
                <EditedBadge
                  editStatus={edit_status}
                  onClick={this.handleUndoEditClick}
                  showEditButtons={this.props.showEditButtons}
                />
              </div>
            )}
            
            {this.props.showEditButtons && (
              <div className="absolute top-0 right-0 ph3 pv3">
                <EditButton
                  actionName="Edit Case"
                  onClick={() => {
                    this.props.whenEditing();
                    this.setState({ editing: true });
                  }}
                />
              </div>
            )}

            <div className="flex-l ph3 pb2">
              <div className="w-100 w-40-l relative pr6 pr4-l">
                {buildRecordTime()}
                <TypeEligibility
                  type_eligibility={expungement_result.type_eligibility}
                  type_name={type_name}
                />
              </div>
              <div className="w-100 w-60-l pr3 pr6-l">
                <ul className="list">
                  <li className="flex mb2">
                    <span className="w6rem shrink-none fw7">Charge</span>
                    {`${statute}${statute && "-"}${name}`}
                  </li>
                  {buildDisposition(disposition)}
                  <li className="flex mb2">
                    <span className="w6rem shrink-none fw7">Charged</span>{" "}
                    {date}
                  </li>
                  <li className="flex mb2">
                    <span className="w6rem shrink-none fw7">Severity</span>{" "}
                    {level}
                  </li>
                </ul>
              </div>
            </div>

            <ExpungementRules expungement_rules={expungement_rules} />
          </>
        )}
        {this.state.editing && (
          <EditChargePanel
            charge={this.props.charge}
            isNewCharge={this.props.isNewCharge}
            whenDoneEditing={() => {
              this.setState({ editing: false });
              this.props.whenDoneEditing();
            }}
            handleUndoEditClick={() => {
              this.handleUndoEditClick();
            }}
          />
        )}

        {!this.state.editing &&
          this.props.charge.edit_status === "UNCHANGED" && (
            <Questions ambiguous_charge_id={ambiguous_charge_id} />
          )}
      </div>
    );
  }
}
