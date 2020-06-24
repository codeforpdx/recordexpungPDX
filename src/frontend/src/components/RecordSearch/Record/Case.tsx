import React from "react";
import { CaseData, ChargeData } from "./types";
import Charges from "./Charges";
import Charge from "./Charge";
import EditCasePanel from "./EditCasePanel";
import EditButton from "./EditButton";
import AddButton from "./AddButton";
import EditedBadge from "./EditedBadge";
import currencyFormat from "../../../service/currency-format";
import { undoEditCase } from "../../../redux/search/actions";
import store from "../../../redux/store";

interface Props {
  case: CaseData;
  editingRecord: boolean;
  editing: boolean;
  isNewCase: boolean;
  whenEditing: Function;
  whenDoneEditing: Function;
}

interface State {
  editing: Boolean;
  addingNewCharge: boolean;
  nextNewChargeNum: number;
  nextBlankCharge: ChargeData;
}
export default class Case extends React.Component<Props, State> {
  createNextBlankCharge = (nextNum: number) => {
    return {
      case_number: this.props.case.case_number,
      ambiguous_charge_id:
        this.props.case.case_number + "-X" + ("00" + nextNum).slice(-2),
      statute: "",
      expungement_result: null,
      name: "",
      type_name: "",
      date: "",
      disposition: {
        status: "",
        ruling: "",
        date: "",
      },
      probation_revoked: "",
      edit_status: "ADD",
    };
  };
  state: State = {
    editing: this.props.editing,
    addingNewCharge: false,
    nextNewChargeNum: 1,
    nextBlankCharge: this.createNextBlankCharge(1),
  };

  handleCaseEditSubmit = () => {
    this.setState({ editing: false });
    this.props.whenDoneEditing();
  };

  handleUndoEditClick = () => {
    if (
      !(this.props.case.edit_status === "ADD") ||
      window.confirm("This data will be lost. Remove anyway?")
    ) {
      store.dispatch(undoEditCase(this.props.case.case_number));
      this.props.whenDoneEditing();
    }
  };

  render() {
    const {
      name,
      case_number,
      birth_year,
      case_detail_link,
      balance_due,
      charges,
      location,
      current_status,
      edit_status,
    } = this.props.case;
    const allIneligible = charges.every(
      (charge) =>
        charge.expungement_result.type_eligibility.status === "Ineligible"
    );
    const prefix = window.location.href.includes("localhost")
      ? "http://localhost:5000"
      : ""; // Hack so we do not have to use nginx for dev
    const case_detail_base =
      "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";
    const link_id = case_detail_link.substring(case_detail_base.length);
    return (
      <div id={case_number} className="mb3">
        <div className="cf pv2 br3 br--top shadow-case">
          {this.props.editing ? null : (
            <>
              <div className="fl ph3 pv1">
                <div className="fw7">Case </div>

                <a
                  href={prefix + "/api/case_detail_page/" + link_id}
                  target="_blank"
                  className="link bb hover-blue"
                >
                  {case_number}
                </a>
              </div>
              <div className="fl ph3 pv1">
                <div className="fw7">Status </div>
                {current_status}
              </div>
              <div className="fl ph3 pv1">
                <div className="fw7">County </div>
                {location}
              </div>
              <div className="fl ph3 pv1">
                <div className="fw7">Balance </div>
                {currencyFormat(balance_due)}
              </div>
              <div className="fl ph3 pv1">
                <div className="fw7">Name </div>
                {name}
              </div>
              <div className="fl ph3 pv1">
                <div className="fw7">DOB </div>
                {birth_year}
              </div>
            </>
          )}
          {edit_status === "UNCHANGED" || this.props.editing ? null : (
            <EditedBadge
              editStatus={edit_status}
              onClick={this.handleUndoEditClick}
              editingRecord={this.props.editingRecord}
            />
          )}
          {this.props.editingRecord || this.state.addingNewCharge ? null : (
            <div className="fl fr-l ph3 pv3">
              <EditButton
                actionName="Edit Case"
                onClick={() => {
                  this.setState({ editing: true });
                  this.props.whenEditing();
                }}
                ariaControls={"case_edit_" + this.props.case.case_number}
              />
              <AddButton
                actionName="Add Charge"
                onClick={() => {
                  this.props.whenEditing();
                  this.setState({ addingNewCharge: true });
                }}
                ariaControls={this.state.nextBlankCharge.ambiguous_charge_id}
              />
            </div>
          )}
        </div>

        {balance_due > 0 && !allIneligible ? (
          <div className="bg-washed-red fw6 br3 pv2 ph3 ma2">
            Eligible charges are ineligible until balance is paid
          </div>
        ) : (
          ""
        )}
        {this.state.editing && (
          <EditCasePanel
            propogateSubmit={this.handleCaseEditSubmit}
            case={this.props.case}
            isNewCase={this.props.isNewCase}
            editStatus={edit_status}
          />
        )}
        {this.state.addingNewCharge && (
          <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
            <Charge
              charge={this.state.nextBlankCharge}
              editingRecord={this.props.editingRecord}
              whenEditing={() => {
                this.props.whenEditing();
              }}
              whenDoneEditing={() => {
                this.props.whenDoneEditing();
                this.setState({
                  addingNewCharge: false,
                  nextNewChargeNum: this.state.nextNewChargeNum + 1,
                  nextBlankCharge: this.createNextBlankCharge(
                    this.state.nextNewChargeNum + 1
                  ),
                });
              }}
              editing={true}
              isNewCharge={true}
            />
          </div>
        )}
        <Charges
          charges={charges}
          editingRecord={this.props.editingRecord}
          whenEditing={() => {
            this.props.whenEditing();
          }}
          whenDoneEditing={() => {
            this.props.whenDoneEditing();
          }}
        />
      </div>
    );
  }
}
