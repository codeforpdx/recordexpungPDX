import React from 'react';
import moment from 'moment';
import { CaseData } from './types';
import InvalidInput from '../../InvalidInput'

interface Props {
  propogateSubmit: Function
  case: CaseData
  }

interface State {
  status: string;
  balance: string;
  birth_year: string;
  county: string;
  missingStatus: boolean;
  missingBalance: boolean;
  invalidBalance: boolean;
  missingBirthYear: boolean;
  invalidBirthYear: boolean;
  }

export default class CaseEditPanel extends React.Component<Props, State> {

  state : State  = {
    status: "",
    balance: "",
    birth_year: "",
    county: "",
    missingStatus: false,
    missingBalance: false,
    invalidBalance: false,
    missingBirthYear: false,
    invalidBirthYear: false,
  };
  handleUpdateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then(() => {
      if (
        !this.state.missingStatus &&
        !this.state.missingBalance &&
        !this.state.missingBirthYear &&
        !this.state.invalidBirthYear
      ) {
          alert("Redux/axios update wizwaz");
          this.props.propogateSubmit();
      }


    });

  };

  handleRemove = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Redux/axios remove wizwaz");
    this.props.propogateSubmit();
  };

  handleCancel = (e: React.FormEvent) => {
    e.preventDefault();
    this.props.propogateSubmit();
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      [e.target.name]: e.target.value
    });
  };

  validateForm = () => {
    return new Promise(resolve => {
      this.setState(
        {
            missingStatus: this.state.status.length === 0,
            missingBalance: this.state.balance.length === 0,
            missingBirthYear: this.state.birth_year.length === 0,
            invalidBirthYear:
            this.state.birth_year !== "" && !moment(this.state.birth_year, 'YYYY', true).isValid()
        },
        resolve
      );
    });
  };

  render() {
    return (
      <div data-reach-disclosure-panel="" data-state="open" id={"case_edit_"+this.props.case.case_number} tabIndex={-1}>
      <form className=" bb bw1 b--black-025 pa3">
        <fieldset className="mw6 pa0">
          <legend className="visually-hidden">Edit Case</legend>

          <div className="mw5 mb3">
            <label htmlFor={"case_edit_number_"+this.props.case.case_number} className="db fw7 mb1">
              Case Number <span className="normal">(Optional)</span>
            </label>
            <input name = "case_number" id={"case_edit_number_"+this.props.case.case_number} type="text" className="w-100 br2 b--black-20 pa3" onChange={this.handleChange}/>
          </div>

          <fieldset className="mb3 pa0">
            <legend className="fw7">Current Status</legend>
            <div className="radio">
              <div className="dib">
                <input type="radio" name="status" id={"case_edit_status_open_"+this.props.case.case_number} value="status-open" onChange={this.handleChange}/>
                <label htmlFor={"case_edit_status_open_"+this.props.case.case_number}>Open</label>
              </div>
              <div className="dib">
                <input type="radio" name="status" id={"case_edit_status_closed_"+this.props.case.case_number} value="status-closed" onChange={this.handleChange}/>
                <label htmlFor={"case_edit_status_closed_"+this.props.case.case_number}>Closed</label>
              </div>
            </div>
          </fieldset>

          <div className="mw5 mb3">
            <label htmlFor={"case_edit_county_"+this.props.case.case_number} className="db mb1 fw7">County</label>
            <div className="relative mb3">
              <select name = "county" id={"case_edit_county_"+this.props.case.case_number} className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white" onChange={this.handleChange}>
                <option value="option1">Option 1</option>
                <option value="option2">Option 2</option>
                <option value="option3">Option 3</option>
              </select>
              <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                <i aria-hidden="true" className="fas fa-angle-down"></i>
              </div>
            </div>
          </div>

          <div className="mw5 mb3">
            <label htmlFor={"case_edit_balance_"+this.props.case.case_number} className="db fw7 mb1">
              Balance
            </label>
            <div className="relative">
              <div className="absolute top-0 bottom-0 pl3 flex items-center">
                <span>$</span>
              </div>
              <input name="balance" id={"case_edit_balance_"+this.props.case.case_number} type="text" className="w-100 br2 b--black-20 pa3 pl4" required aria-invalid="false" onChange={this.handleChange}/>
            </div>
          </div>

          <div className="mw5 mb4">
            <label htmlFor={"case_edit_birthyear_"+this.props.case.case_number} className="db fw7 mb1">
              Birth Year <span className="normal">yyyy</span>
            </label>
            <input name="birth_year" id={"case_edit_birthyear_"+this.props.case.case_number} type="number" className="w-100 br2 b--black-20 pa3" required aria-invalid="false" onChange={this.handleChange}/>
          </div>

          <div className="flex items-center mb3">
            <button className="fw6 br2 bg-blue white bg-animate hover-bg-dark-blue pa3 mr4" onClick={this.handleUpdateSubmit}>
              Update Case
            </button>
            <button className="fw6 blue link hover-red mr4" onClick={this.handleRemove}>
              Remove Case
            </button>
            <button className="fw6 blue link hover-dark-blue mr4" onClick={this.handleCancel}>
              Cancel
            </button>
          </div>

          <InvalidInput message="Current Status is required" condition={this.state.missingStatus}/>
          <InvalidInput message="Balance is required" condition={this.state.missingBalance}/>
          <InvalidInput message="Birth Year is required" condition={this.state.missingBirthYear}/>
          <InvalidInput message="Birth Year format is invalid" condition={this.state.invalidBirthYear}/>
        </fieldset>
      </form>
    </div>
    );
  }
}
