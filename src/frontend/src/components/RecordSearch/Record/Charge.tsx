import React from "react";
import Eligibility from "./Eligibility";
import TimeEligibility from "./TimeEligibility";
import TypeEligibility from "./TypeEligibility";
import EditChargePanel from "./EditChargePanel";
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
      expungement_result,
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
      <div className="br3 ma2 bg-white" id={ambiguous_charge_id}>
        {this.props.isNewCharge ? null : (
          <>
            {edit_status !== "DELETE" && (
              <Eligibility
                expungement_result={expungement_result}
                removed={edit_status === "DELETE"}
              />
            )}
            {edit_status !== "UNCHANGED" && (
              <EditedBadge
                editStatus={edit_status}
                onClick={this.handleUndoEditClick}
                showEditButtons={this.props.showEditButtons}
              />
            )}
            <div className="dib fr-ns ph2 pv3">
              {this.props.showEditButtons && (
                <EditButton
                  actionName="Edit Case"
                  onClick={() => {
                    this.props.whenEditing();
                    this.setState({ editing: true });
                  }}
                />
              )}
            </div>

            <div className="flex-l ph3 pb3">
              <div className="w-100 w-40-l relative pr3">
                {buildRecordTime()}
                <TypeEligibility
                  type_eligibility={expungement_result.type_eligibility}
                  type_name={type_name}
                />
              </div>
              <div className="w-100 w-60-l pr3">
                <ul className="list">
                  <li className="flex mb2">
                    <span className="w6rem shrink-none fw7">Charge</span>
                    {`${statute}${statute && "-"}${name}`}
                  </li>
                  {buildDisposition(disposition)}
                  <li className="flex mb2">
                    <span className="w6rem shrink-none fw7">Charged</span> {date}
                  </li>
                </ul>
              </div>
            </div>
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
