import React from "react";
import { HashLink as Link } from "react-router-hash-link";
import {
  ChargeData,
  CHARGE_TYPES,
  CHARGE_TYPES_CONVICTED_ONLY,
  CHARGE_TYPES_DISMISSED_ONLY,
  SEVERITY_LEVELS,
} from "./types";
import { isDate } from "../../../service/validators";
import InvalidInputs from "../../InvalidInputs";
import { editCharge, deleteCharge } from "../../../redux/search/actions";
import DateField from "./DateField";

import store from "../../../redux/store";

interface Props {
  charge: ChargeData;
  isNewCharge: boolean;
  whenDoneEditing: Function;
  handleUndoEditClick: Function;
}

interface State {
  edit_status: string;
  date: string;
  disposition_status: string;
  disposition_date: string;
  probation_revoked_date: string;
  name: string;
  type_name: string;
  level: string;
  missingDisposition: boolean;
  missingType: boolean;
  missingLevel: boolean;
  missingDate: boolean;
  invalidDate: boolean;
  missingDispositionDate: boolean;
  invalidDispositionDate: boolean;
  missingProbationRevoked: boolean;
  invalidProbationRevoked: boolean;
}

const shortToMMDDYYYY = (shortDate: string) => {
  if (!shortDate || isNaN(Date.parse(shortDate))) return "";
  const date = new Date(Date.parse(shortDate));
  return (
    (date.getMonth() + 1).toString() +
    "/" +
    date.getDate().toString() +
    "/" +
    date.getFullYear().toString()
  );
};

export default class EditChargePanel extends React.Component<Props, State> {
  state: State = {
    edit_status: this.props.charge.edit_status,
    date: shortToMMDDYYYY(this.props.charge.date),
    disposition_status: this.props.charge.disposition.status,
    disposition_date: shortToMMDDYYYY(this.props.charge.disposition.date),
    probation_revoked_date: shortToMMDDYYYY(
      this.props.charge.probation_revoked
    ),
    name: this.props.charge.name,
    type_name: CHARGE_TYPES.includes(this.props.charge.type_name)
      ? this.props.charge.type_name
      : "",
    level: SEVERITY_LEVELS.includes(this.props.charge.level)
      ? this.props.charge.level
      : "",
    missingDate: false,
    invalidDate: false,
    missingDisposition: false,
    missingType: false,
    missingLevel: false,
    missingDispositionDate: false,
    invalidDispositionDate: false,
    missingProbationRevoked: false,
    invalidProbationRevoked: false,
  };

  anyFieldsChanged = () => {
    return !(
      shortToMMDDYYYY(this.props.charge.date) === this.state.date &&
      shortToMMDDYYYY(this.props.charge.disposition.date) ===
        this.state.disposition_date &&
      shortToMMDDYYYY(this.props.charge.probation_revoked) ===
        this.state.probation_revoked_date &&
      this.props.charge.disposition.status === this.state.disposition_status &&
      this.props.charge.name === this.state.name &&
      this.props.charge.type_name === this.state.type_name &&
      this.props.charge.level === this.state.level
    );
  };

  handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!this.anyFieldsChanged()) {
      this.props.whenDoneEditing();
      return;
    }
    this.validateForm().then(() => {
      if (
        !this.state.missingDisposition &&
        !this.state.missingType &&
        !this.state.missingLevel &&
        !this.state.missingDate &&
        !this.state.invalidDate &&
        !this.state.missingDispositionDate &&
        !this.state.invalidDispositionDate &&
        !this.state.missingProbationRevoked &&
        !this.state.invalidProbationRevoked
      ) {
        this.dispatchEdit();
        this.props.whenDoneEditing();
      }
    });
  };

  dispatchEdit = () => {
    store.dispatch(
      editCharge(
        this.props.isNewCharge || this.props.charge.edit_status === "ADD"
          ? "ADD"
          : "UPDATE",
        this.props.charge.case_number,
        this.props.charge.ambiguous_charge_id,
        this.state.date,
        this.state.disposition_status === "Probation Revoked"
          ? "Convicted"
          : this.state.disposition_status,
        this.state.disposition_date,
        this.state.probation_revoked_date,
        this.state.type_name,
        this.state.level,
        this.state.name
      )
    );
  };

  dispatchDelete = () => {
    store.dispatch(
      deleteCharge(
        this.props.charge.case_number,
        this.props.charge.ambiguous_charge_id
      )
    );
  };

  handleRemove = (e: React.FormEvent) => {
    e.preventDefault();
    if (this.state.edit_status === "ADD") {
      this.props.handleUndoEditClick();
    } else {
      this.dispatchDelete();
    }
    this.props.whenDoneEditing();
  };

  handleCancel = (e: React.FormEvent) => {
    e.preventDefault();
    this.props.whenDoneEditing();
  };

  handleDispositionStatusChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      missingDispositionDate: false,
      invalidDispositionDate: false,
      missingProbationRevoked: false,
      invalidProbationRevoked: false,
      disposition_date:
        e.target.value === "Dismissed" || e.target.value === "Convicted"
          ? ""
          : shortToMMDDYYYY(this.props.charge.disposition.date),
      probation_revoked_date: "",
      [e.target.name]: e.target.value,
      type_name:
        (e.target.value === "Dismissed" &&
          CHARGE_TYPES_CONVICTED_ONLY.includes(this.state.type_name)) ||
        (e.target.value === "Convicted" &&
          CHARGE_TYPES_DISMISSED_ONLY.includes(this.state.type_name))
          ? ""
          : this.state.type_name,
    });
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      [e.target.name]: e.target.value,
    });
  };

  validateForm = () => {
    return new Promise((resolve: (value?: unknown) => void) => {
      this.setState(
        {
          missingDisposition: this.state.disposition_status === "",
          missingType: this.state.type_name === "",
          missingLevel: this.state.level === "",
          missingDate: this.state.date === "",
          invalidDate: this.state.date !== "" && !isDate(this.state.date),
          missingDispositionDate:
            (this.state.disposition_status === "Convicted" ||
              this.state.disposition_status === "Probation Revoked") &&
            this.state.disposition_date === "",
          invalidDispositionDate:
            this.state.disposition_date !== "" &&
            !isDate(this.state.disposition_date),
          missingProbationRevoked:
            this.state.disposition_status === "Probation Revoked" &&
            this.state.probation_revoked_date === "",
          invalidProbationRevoked:
            this.state.probation_revoked_date !== "" &&
            !isDate(this.state.probation_revoked_date),
        },
        resolve
      );
    });
  };

  render() {
    return (
      <div
        id={"edit-charge-panel-" + this.props.charge.ambiguous_charge_id}
        tabIndex={-1}
      >
        <form className="pa3" noValidate>
          <fieldset className="mw7 pa0">
            <legend className="visually-hidden">Edit Charge</legend>
            <fieldset className="mb3 pa0">
              <legend className="fw6">Disposition</legend>
              <div className="radio">
                {["Convicted", "Dismissed", "Probation Revoked", "Missing"].map(
                  (status: string, index: number) => {
                    const id =
                      this.props.charge.ambiguous_charge_id + "-edit-" + status;
                    return (
                      <div className="dib" key={index}>
                        <input
                          type="radio"
                          name="disposition_status"
                          defaultChecked={
                            status === this.state.disposition_status
                          }
                          id={id}
                          value={status}
                          onChange={this.handleDispositionStatusChange}
                        />
                        <label htmlFor={id}>
                          {status === "Missing" ? "Unknown" : status}
                        </label>
                      </div>
                    );
                  }
                )}
              </div>
            </fieldset>
            {(this.state.disposition_status === "Convicted" ||
              this.state.disposition_status === "Probation Revoked") && (
              <div className="mb3">
                <DateField
                  fieldLabel="Conviction Date"
                  onChange={(dateVal: string) => {
                    this.setState({ disposition_date: dateVal });
                  }}
                  inputId={
                    "edit-dispo-date-" + this.props.charge.ambiguous_charge_id
                  }
                  value={this.state.disposition_date}
                />
              </div>
            )}
            {this.state.disposition_status === "Probation Revoked" && (
              <div className="mb3">
                <DateField
                  fieldLabel="Probation Revoked"
                  onChange={(dateVal: string) => {
                    this.setState({ probation_revoked_date: dateVal });
                  }}
                  inputId={
                    "edit-probation-revoked-" +
                    this.props.charge.ambiguous_charge_id
                  }
                  value={this.state.probation_revoked_date}
                />
              </div>
            )}
            <div className="mw6 mb3">
              <label
                htmlFor={
                  this.props.charge.ambiguous_charge_id + "-select-charge-type"
                }
                className="db mb1 fw6"
              >
                Charge Type
                <Link
                  to="/rules#chargetypes"
                  className=" gray link hover-blue underline"
                >
                  <i
                    aria-hidden="true"
                    className="fas fa-question-circle link hover-dark-blue gray pl1"
                  ></i>
                </Link>
              </label>
              <div className="relative mb3">
                <select
                  id={
                    this.props.charge.ambiguous_charge_id +
                    "-select-charge-type"
                  }
                  value={this.state.type_name}
                  name="type_name"
                  onChange={this.handleChange}
                  className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white"
                  required
                  aria-invalid="false"
                >
                  <option value="">Select...</option>
                  {CHARGE_TYPES.map((type_name, i) => (
                    <option
                      value={type_name}
                      key={i}
                      disabled={
                        (this.state.disposition_status === "Dismissed" &&
                          CHARGE_TYPES_CONVICTED_ONLY.includes(type_name)) ||
                        (["Convicted", "Probation Revoked"].includes(
                          this.state.disposition_status
                        ) &&
                          CHARGE_TYPES_DISMISSED_ONLY.includes(type_name))
                      }
                    >
                      {type_name}
                    </option>
                  ))}
                </select>
                <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                  <i aria-hidden="true" className="fas fa-angle-down"></i>
                </div>
              </div>
            </div>
            <div className="mw6 mb3">
              <label
                htmlFor={
                  this.props.charge.ambiguous_charge_id + "-select-level"
                }
                className="db mb1 fw6"
              >
                Severity Level
                <Link
                  to="/rules#chargetypes"
                  className=" gray link hover-blue underline"
                >
                  <i
                    aria-hidden="true"
                    className="fas fa-question-circle link hover-dark-blue gray pl1"
                  ></i>
                </Link>
              </label>

              <div className="relative mb3">
                <select
                  id={this.props.charge.ambiguous_charge_id + "-select-level"}
                  value={this.state.level}
                  name="level"
                  onChange={this.handleChange}
                  className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white"
                  required
                  aria-invalid="false"
                >
                  <option value="">Select...</option>
                  {SEVERITY_LEVELS.map((level, i) => (
                    <option value={level} key={i}>
                      {level}
                    </option>
                  ))}
                </select>
                <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                  <i aria-hidden="true" className="fas fa-angle-down"></i>
                </div>
              </div>
            </div>
            <div className="mw6 mb3">
              <label htmlFor="charge-name" className="db mb1 fw6">
                Charge Name <span className="fw3">(Optional)</span>
              </label>
              <div className="relative mb3">
                <input
                  id="name"
                  className="w-100 br2 b--black-20 pa3"
                  value={this.state.name}
                  name="name"
                  required
                  aria-invalid="false"
                  onChange={this.handleChange}
                />
              </div>
            </div>
            <div className="mw5 mb4">
              <label htmlFor="date-charged" className="db fw6 mb1">
                Date Charged <span className="normal">mm/dd/yyyy</span>
              </label>
              <input
                id="date-charged"
                name="date"
                value={this.state.date}
                onChange={this.handleChange}
                className="w-100 br2 b--black-20 pa3"
                required
                aria-invalid="false"
              />
            </div>
            <div className="flex items-center mb3">
              <button
                className="fw6 br2 bg-blue white bg-animate hover-bg-dark-blue pa3 mr4"
                onClick={this.handleEditSubmit}
              >
                {this.props.isNewCharge ? "Add Charge" : "Update Charge"}
              </button>
              {this.props.isNewCharge ? null : (
                <button
                  className="fw6 blue link hover-red mr4"
                  onClick={this.handleRemove}
                >
                  Remove Charge
                </button>
              )}
              <button
                className="fw6 blue link hover-dark-blue mr4"
                onClick={this.handleCancel}
              >
                Cancel
              </button>
            </div>
            <InvalidInputs
              conditions={[
                this.state.missingType,
                this.state.missingLevel,
                this.state.missingDate,
                this.state.invalidDate,
                this.state.missingDisposition,
                this.state.missingDispositionDate,
                this.state.invalidDispositionDate,
                this.state.missingProbationRevoked,
                this.state.invalidProbationRevoked,
              ]}
              contents={[
                <span>Charge Type is required</span>,
                <span>Charge Severity Level is required</span>,
                <span>Date Charged is required</span>,
                <span>Date Charged format is invalid</span>,
                <span>Disposition is required</span>,
                <span>Disposition date is required</span>,
                <span>Disposition date format is invalid</span>,
                <span>Probation Revoked date is required</span>,
                <span>Probation Revoked date format is invalid</span>,
              ]}
            />{" "}
          </fieldset>
        </form>
      </div>
    );
  }
}
