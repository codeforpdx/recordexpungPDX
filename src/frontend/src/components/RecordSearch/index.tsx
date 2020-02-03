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
    this.validateForm().then(() => {
      if (
        this.state.missingInputs === false &&
        this.state.invalidDate === false
      ) {
        // Dispatch an action.
        let state = this.state;
        let firstName = state.firstName;
        let lastName = state.lastName;
        let dateOfBirth = state.dateOfBirth.length > 0 ? state.dateOfBirth : '';
        this.props.fetchRecords(firstName, lastName, dateOfBirth);
      }
    });
  };

  validateForm = () => {
    return new Promise(resolve => {
      this.setState(
        {
          firstNameHasInput: this.state.firstName.trim().length === 0,
          lastNameHasInput: this.state.lastName.trim().length === 0,
          missingInputs:
            this.state.firstName.trim().length === 0 ||
            this.state.lastName.trim().length === 0,
          invalidDate:
            moment(this.state.dateOfBirth, 'M/D/YYYY', true).isValid() ===
              false && this.state.dateOfBirth.length !== 0
        },
        resolve
      );
    });
  };

  public render() {
    return (
      <div>
        <h1 className="f4 fw6 tc mv4">Record Search</h1>
        <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
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

        <section className="cf mt4 mb3 pa3 pa4-ns bg-white shadow br3">
          <form className="mw7 center">
            <div className="flex flex-wrap items-end">
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="first-name" className="db mb1 fw6">
                  First Name
                </label>
                <input id="first-name" type="text" className="w-100 b--black-20 br2 br-0-ns br--left-ns pa3" required aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="middle-name" className="db mb1 fw6">
                  Middle Name
                </label>
                <input id="middle-name" type="text" className="w-100 pa3 b--black-20" aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="last-name" className="db mb1 fw6">
                  Last Name
                </label>
                <input id="last-name" type="text" className="w-100 b--black-20 br2 bl-0-ns br--right-ns pa3" required aria-invalid="false" />
              </div>
            </div>
            <div className="flex flex-wrap items-center">
              <div className="w-100 w-third-ns mb2 mb3-ns">
                <label htmlFor="date-of-birth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input id="date-of-birth" type="text" className="w-100 pa3 br2 b--black-20" required aria-describedby="dob_msg" aria-invalid="false" />
              </div>
              <div className="flex justify-between w-100 w-two-thirds-ns">
                <div className="fw5 center-ns pr3 pt3 pa3-ns mt2-ns">
                </div>
                <div className="mb3 mt2-ns">
                  <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv2 ph3 mt2 ml2">
                    <i aria-hidden="true" className="fas fa-plus-circle" />
                    &nbsp;Search
                  </button>
                </div>
              </div>
            </div>
            <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search" type="submit">
              <i aria-hidden="true" className="fas fa-search pr2" />
              <span className="fw7">Search Records</span>
            </button>
            <div role="alert">
            </div>
          </form>
        </section>
        <section className="cf mt4 mb3 pa3 pa4-ns bg-white shadow br3">
          <form className="mw7 center">
            <div className="flex flex-wrap items-end">
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="first-name" className="db mb1 fw6">
                  First Name
                </label>
                <input id="first-name" type="text" className="w-100 b--black-20 br2 br-0-ns br--left-ns pa3" required aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="middle-name" className="db mb1 fw6">
                  Middle Name
                </label>
                <input id="middle-name" type="text" className="w-100 pa3 b--black-20" aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="last-name" className="db mb1 fw6">
                  Last Name
                </label>
                <input id="last-name" type="text" className="w-100 b--black-20 br2 bl-0-ns br--right-ns pa3" required aria-invalid="false" />
              </div>
            </div>
            <div className="flex flex-wrap items-center">
              <div className="w-100 w-third-ns mb2 mb3-ns pr2-ns">
                <label htmlFor="date-of-birth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input id="date-of-birth" type="text" className="w-100 pa3 br2 b--black-20" required aria-describedby="dob_msg" aria-invalid="false" />
              </div>
              <div className="flex justify-between w-100 w-two-thirds-ns">
                <div className="fw5 pr3 pt3 pa3-ns mt2-ns">
                  2 Unique Results
                </div>
                <div className="mb3 mt2-ns">
                  <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv2 ph3 mt2">
                    <i aria-hidden="true" className="fas fa-times-circle" />
                    &nbsp;Remove
                  </button>
                </div>
              </div>
            </div>
            <hr className="bb b--black-05 mt2 mt3-ns mb3 mb4-ns" />
            <div className="flex flex-wrap items-end">
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="first-name" className="db mb1 fw6">
                  First Name
                </label>
                <input id="first-name" type="text" className="w-100 b--black-20 br2 br-0-ns br--left-ns pa3" required aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="middle-name" className="db mb1 fw6">
                  Middle Name
                </label>
                <input id="middle-name" type="text" className="w-100 pa3 b--black-20" aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="last-name" className="db mb1 fw6">
                  Last Name
                </label>
                <input id="last-name" type="text" className="w-100 b--black-20 br2 bl-0-ns br--right-ns pa3" required aria-invalid="false" />
              </div>
            </div>
            <div className="flex flex-wrap items-center">
              <div className="w-100 w-third-ns mb2 mb3-ns pr2-ns">
                <label htmlFor="date-of-birth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input id="date-of-birth" type="text" className="w-100 pa3 br2 b--black-20" required aria-describedby="dob_msg" aria-invalid="false" />
              </div>
              <div className="flex justify-between w-100 w-two-thirds-ns">
                <div className="fw5 pr3 pt3 pa3-ns mt2-ns">
                  1 Unique Result
                </div>
                <div className="mb3 mt2-ns">
                  <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv2 ph3 mt2">
                    <i aria-hidden="true" className="fas fa-times-circle" />
                    &nbsp;Remove
                  </button>
                </div>
              </div>
            </div>
            <hr className="bb b--black-05 mt2 mt3-ns mb3 mb4-ns" />
            <div className="flex flex-wrap items-end">
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="first-name" className="db mb1 fw6">
                  First Name
                </label>
                <input id="first-name" type="text" className="w-100 b--black-20 br2 br-0-ns br--left-ns pa3" required aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="middle-name" className="db mb1 fw6">
                  Middle Name
                </label>
                <input id="middle-name" type="text" className="w-100 pa3 b--black-20" aria-invalid="false" />
              </div>
              <div className="w-100 w-third-ns mb3">
                <label htmlFor="last-name" className="db mb1 fw6">
                  Last Name
                </label>
                <input id="last-name" type="text" className="w-100 b--black-20 br2 bl-0-ns br--right-ns pa3" required aria-invalid="false" />
              </div>
            </div>
            <div className="flex flex-wrap items-center">
              <div className="w-100 w-third-ns mb2 mb3-ns pr2-ns">
                <label htmlFor="date-of-birth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input id="date-of-birth" type="text" className="w-100 pa3 br2 b--black-20" required aria-describedby="dob_msg" aria-invalid="false" />
              </div>
              <div className="flex justify-between w-100 w-two-thirds-ns">
                <div className="fw5 pr3 pt3 pa3-ns mt2-ns">
                  2 Unique Results
                </div>
                <div className="mb3 mt2-ns">
                  <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv2 ph3 mt2">
                    <i aria-hidden="true" className="fas fa-times-circle" />
                    &nbsp;Remove
                  </button>
                  <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv2 ph3 mt2 ml2">
                    <i aria-hidden="true" className="fas fa-plus-circle" />
                    &nbsp;Search
                  </button>
                </div>
              </div>
            </div>
            <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search" type="submit">
              <i aria-hidden="true" className="fas fa-search pr2" />
              <span className="fw7">Search Records</span>
            </button>
            <div role="alert">
            </div>
          </form>
        </section>

      </div>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(mapStateToProps)(RecordSearch);
