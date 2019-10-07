import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { SystemState } from '../../redux/system/types';
import moment from 'moment';

interface Props {
  system: SystemState;
  fetchRecords: Function;
}

interface State {
  firstName: string;
  lastName: string;
  dateOfBirth: string;
  firstNameHasInput: boolean;
  lastNameHasInput: boolean;
  missingInputs: null | boolean;
  invalidDate: boolean;
}

class RecordSearch extends React.Component<Props, State> {
  state: State = {
    firstName: '',
    lastName: '', // Validation check relies on string length.
    dateOfBirth: '', // Moment expects a string to be passed in as a paramenter in the validateForm function.
    firstNameHasInput: false, // Initially set to false to ensure aria-invalid attribute is rendered.
    lastNameHasInput: false,
    missingInputs: null,
    invalidDate: false
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value
    });
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm();
    if (
      this.state.missingInputs === false &&
      this.state.invalidDate === false
    ) {
      // Dispatch an action.
      this.props.fetchRecords();
    }
  };

  validateForm = () => {
    this.setState({
      firstNameHasInput: this.state.firstName.trim().length === 0
    });
    this.setState({
      lastNameHasInput: this.state.lastName.trim().length === 0
    });
    this.setState({
      missingInputs:
        this.state.firstName.trim().length === 0 ||
        this.state.lastName.trim().length === 0 ||
        this.state.dateOfBirth.trim().length === 0
    });
    this.setState({
      invalidDate:
        moment(this.state.dateOfBirth, 'MM/DD/YYYY', true).isValid() === false
    });
  };

  public render() {
    return (
      <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
        <h1 className="mb4 f4 fw6">Record Search</h1>
        <form onSubmit={this.handleSubmit} noValidate>
          <div className="flex flex-wrap items-end">
            <div className="w-100 w-30-ns mb3 pr2-ns">
              <label htmlFor="firstName" className="db mb1 fw6">
                First Name
              </label>
              <input
                id="firstName"
                type="text"
                className="w-100 pa3 br2 b--black-20"
                required
                aria-describedby={
                  this.state.firstNameHasInput ? 'name_msg' : undefined
                }
                aria-invalid={this.state.firstNameHasInput}
                onChange={this.handleChange}
              />
            </div>
            <div className="w-100 w-30-ns mb3 pr2-ns">
              <label htmlFor="lastName" className="db mb1 fw6">
                Last Name
              </label>
              <input
                id="lastName"
                type="text"
                className="w-100 pa3 br2 b--black-20"
                required
                aria-describedby={
                  this.state.lastNameHasInput ? 'name_msg' : undefined
                }
                aria-invalid={this.state.lastNameHasInput}
                onChange={this.handleChange}
              />
            </div>
            <div className="w-100 w-30-ns mb3 pr2-ns">
              <label htmlFor="dateOfBirth" className="db mb1 fw6">
                Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
              </label>
              <input
                id="dateOfBirth"
                type="text"
                className="w-100 pa3 br2 b--black-20"
                required
                aria-describedby={
                  this.state.invalidDate ? 'dob_msg' : undefined
                }
                aria-invalid={this.state.invalidDate}
                onChange={this.handleChange}
              />
            </div>
            <div className="w-100 w-10-ns mb3">
              <button
                className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search"
                type="submit"
              >
                <span className="visually-hidden">Search Records</span>
                <i aria-hidden="true" className="fas fa-search" />
              </button>
            </div>
            <div role="alert" className="w-100">
              {this.state.missingInputs === true ? (
                <p id="name_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  All search fields are required.
                </p>
              ) : null}
              {this.state.invalidDate === true ? (
                <p id="dob_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  The date format must be MM/DD/YYYY.
                </p>
              ) : null}
            </div>
          </div>
        </form>
      </section>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(mapStateToProps)(RecordSearch);
