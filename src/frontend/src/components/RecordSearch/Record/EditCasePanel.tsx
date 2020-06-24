import React from "react";
import moment from "moment";
import { CaseData } from "./types";
import {
  editCase,
  deleteCase,
  undoEditCase,
} from "../../../redux/search/actions";
import store from "../../../redux/store";
import InvalidInputs from "../../InvalidInputs";

interface Props {
  propogateSubmit: Function;
  case: CaseData;
  isNewCase: boolean;
  editStatus: string;
}

interface State {
  status: string;
  county: string;
  balance: string;
  birth_year: string;
  missingStatus: boolean;
  missingCounty: boolean;
  missingBalance: boolean;
  missingBirthYear: boolean;
  invalidBirthYear: boolean;
}

const counties = [
  "Baker",
  "Benton",
  "Clackamas",
  "Clatsop",
  "Columbia",
  "Coos",
  "Crook",
  "Curry",
  "Deschutes",
  "Douglas",
  "Gilliam",
  "Grant",
  "Harney",
  "Hood River",
  "Jackson",
  "Jefferson",
  "Josephine",
  "Klamath",
  "Lake",
  "Lane",
  "Lincoln",
  "Linn",
  "Malheur",
  "Marion",
  "Morrow",
  "Multnomah",
  "Polk",
  "Sherman",
  "Tillamook",
  "Umatilla",
  "Union",
  "Wallowa",
  "Wasco",
  "Washington",
  "Wheeler",
  "Yamhill",
];

export default class EditCasePanel extends React.Component<Props, State> {
  state: State = {
    status: this.props.case.current_status,
    county: this.props.case.location,
    balance: this.props.case.balance_due.toFixed(2),
    birth_year: this.props.case.birth_year.toString(),
    missingStatus: false,
    missingCounty: false,
    missingBalance: false,
    missingBirthYear: false,
    invalidBirthYear: false,
  };

  handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then(() => {
      if (
        !this.state.missingStatus &&
        !this.state.missingCounty &&
        !this.state.missingBalance &&
        !this.state.missingBirthYear &&
        !this.state.invalidBirthYear
      ) {
        this.dispatchEdit();
        this.props.propogateSubmit();
      }
    });
  };

  dispatchEdit = () => {
    store.dispatch(
      editCase(
        this.props.isNewCase || this.props.case.edit_status === "ADD"
          ? "ADD"
          : "UPDATE",
        this.props.case.case_number,
        this.state.status,
        this.state.county,
        this.state.balance,
        this.state.birth_year
      )
    );
  };

  dispatchDelete = () => {
    store.dispatch(deleteCase(this.props.case.case_number));
  };

  handleRemove = (e: React.FormEvent) => {
    e.preventDefault();
    if (this.props.editStatus == "ADD") {
      if (window.confirm("This data will be lost. Remove anyway?")) {
        store.dispatch(undoEditCase(this.props.case.case_number));
        this.props.propogateSubmit();
      }
    } else {
      this.dispatchDelete();
      this.props.propogateSubmit();
    }
  };

  handleCancel = (e: React.FormEvent) => {
    e.preventDefault();
    this.props.propogateSubmit();
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      [e.target.name]: e.target.value,
    });
  };

  balancePattern = new RegExp("[0-9]*[.]?[0-9]?[0-9]?");
  handleBalanceChange = (e: React.BaseSyntheticEvent) => {
    const parsed = this.balancePattern.exec(e.target.value);
    this.setState<any>({
      balance: parsed ? parsed[0] : "",
    });
  };

  birthYearPattern = new RegExp("[0-9][0-9]?[0-9]?[0-9]?");
  handleBirthYearChange = (e: React.BaseSyntheticEvent) => {
    const parsed = this.birthYearPattern.exec(e.target.value);
    this.setState<any>({
      birth_year: parsed ? parsed[0] : "",
    });
  };

  validateForm = () => {
    return new Promise((resolve) => {
      this.setState(
        {
          missingStatus: this.state.status.length === 0,
          missingCounty: this.state.county === "",
          missingBalance: this.state.balance.length === 0,
          missingBirthYear:
            this.state.birth_year.length === 0 || this.state.birth_year == "0",
          invalidBirthYear:
            this.state.birth_year !== "" &&
            this.state.birth_year !== "0" &&
            !moment(this.state.birth_year, "YYYY", true).isValid(),
        },
        resolve
      );
    });
  };

  render() {
    return (
      <div
        data-reach-disclosure-panel=""
        data-state="open"
        id={"case_edit_" + this.props.case.case_number}
        tabIndex={-1}
      >
        <form className="pa3">
          {" "}
          {/* TODO these were in the styling but the mockup doesn't have a border.  bb bw1 b--black-025 */}
          <fieldset className="mw6 pa0">
            <legend className="visually-hidden">Edit Case</legend>
            <fieldset className="mb3 pa0">
              <legend className="fw7">Current Status</legend>
              <div className="radio">
                <div className="dib">
                  <input
                    type="radio"
                    name="status"
                    id={"case_edit_status_open_" + this.props.case.case_number}
                    value="Open"
                    checked={this.state.status === "Open"}
                    onChange={this.handleChange}
                  />
                  <label
                    htmlFor={
                      "case_edit_status_open_" + this.props.case.case_number
                    }
                  >
                    Open
                  </label>
                </div>
                <div className="dib">
                  <input
                    type="radio"
                    name="status"
                    id={
                      "case_edit_status_closed_" + this.props.case.case_number
                    }
                    value="Closed"
                    checked={this.state.status === "Closed"}
                    onChange={this.handleChange}
                  />
                  <label
                    htmlFor={
                      "case_edit_status_closed_" + this.props.case.case_number
                    }
                  >
                    Closed
                  </label>
                </div>
              </div>
            </fieldset>
            <div className="mw5 mb3">
              <label
                htmlFor={"case_edit_county_" + this.props.case.case_number}
                className="db mb1 fw7"
              >
                County
              </label>
              <div className="relative mb3">
                <select
                  value={this.state.county}
                  name="county"
                  id={"case_edit_county_" + this.props.case.case_number}
                  className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white"
                  onChange={this.handleChange}
                >
                  <option value="">---</option>
                  {counties.map((county, index) => {
                    return (
                      <option key={index} value={county}>
                        {county}
                      </option>
                    );
                  })}
                </select>
                <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                  <i aria-hidden="true" className="fas fa-angle-down"></i>
                </div>
              </div>
            </div>
            <div className="mw5 mb3">
              <label
                htmlFor={"case_edit_balance_" + this.props.case.case_number}
                className="db fw7 mb1"
              >
                Balance
              </label>
              <div className="relative">
                <div className="absolute top-0 bottom-0 pl3 flex items-center">
                  <span>$</span>
                </div>
                <input
                  name="balance"
                  value={this.state.balance}
                  id={"case_edit_balance_" + this.props.case.case_number}
                  type="text"
                  className="w-100 br2 b--black-20 pa3 pl4"
                  required
                  aria-invalid="false"
                  onChange={this.handleBalanceChange}
                />
              </div>
            </div>
            <div className="mw5 mb4">
              <label
                htmlFor={"case_edit_birthyear_" + this.props.case.case_number}
                className="db fw7 mb1"
              >
                Birth Year <span className="normal">yyyy</span>
              </label>
              <input
                name="birth_year"
                value={
                  this.props.isNewCase && this.state.birth_year == "0"
                    ? ""
                    : this.state.birth_year
                }
                id={"case_edit_birthyear_" + this.props.case.case_number}
                type="text"
                className="w-100 br2 b--black-20 pa3"
                required
                aria-invalid="false"
                onChange={this.handleBirthYearChange}
              />
            </div>
            <div className="flex items-center mb3">
              <button
                className="fw6 br2 bg-blue white bg-animate hover-bg-dark-blue pa3 mr4"
                onClick={this.handleEditSubmit}
              >
                {this.props.isNewCase ? "Create Case" : "Update Case"}
              </button>
              {this.props.isNewCase ? null : (
                <button
                  className="fw6 blue link hover-red mr4"
                  onClick={this.handleRemove}
                >
                  Remove Case
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
                this.state.missingStatus,
                this.state.missingCounty,
                this.state.missingBalance,
                this.state.missingBirthYear,
                this.state.invalidBirthYear,
              ]}
              contents={[
                <span>Current Status is required</span>,
                <span>County is required</span>,
                <span>Balance is required</span>,
                <span>Birth Year is required</span>,
                <span>Birth Year format is invalid</span>,
              ]}
            />{" "}
          </fieldset>
        </form>
      </div>
    );
  }
}
