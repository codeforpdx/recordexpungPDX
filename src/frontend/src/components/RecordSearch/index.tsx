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
  middleName: string;
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
    middleName: '',
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
        let middleName = state.middleName;
        let lastName = state.lastName;
        let dateOfBirth = state.dateOfBirth.length > 0 ? state.dateOfBirth : '';
        this.props.fetchRecords(firstName, middleName, lastName, dateOfBirth);
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
        <section className="cf mt4 mb3 pa4 bg-white shadow br3">
          <form className="mw7 center" onSubmit={this.handleSubmit} noValidate>
            <div className="flex flex-wrap items-end">

              <div className="w-100 w-third-ns w-25-l mb3">
              { // TODO: abstract this div to a "Field" react component,
                // to instance as First, middle, last name, and bday
              }
                <label htmlFor="firstName" className="db mb1 fw6">
                  First Name
                </label>
                <input
                  id="firstName"
                  type="text"
                  className="w-100 b--black-20 br2 br-0-ns br--left-ns pa3"
                  required
                  aria-describedby={
                    this.state.firstNameHasInput ? 'name_msg' : undefined
                  }
                  aria-invalid={this.state.firstNameHasInput}
                  onChange={this.handleChange}
                />
              </div>
              <div className="w-100 w-third-ns w-25-l mb3">
                <label htmlFor="middleName" className="db mb1 fw6">
                  Middle Name <span className= "fw2 f6">Optional</span>
                </label>
                <input
                  id="middleName"
                  type="text"
                  className="w-100 br2 br0-ns b--black-20 pa3"
                  onChange={this.handleChange}
                />
              </div>
              <div className="w-100 w-third-ns w-25-l mb3">
                <label htmlFor="lastName" className="db mb1 fw6">
                  Last Name
                </label>
                <input
                  id="lastName"
                  type="text"
                  className="w-100 b--black-20 br2 bl-0-ns br--right-ns pa3"
                  required
                  aria-describedby={
                    this.state.lastNameHasInput ? 'name_msg' : undefined
                  }
                  aria-invalid={this.state.lastNameHasInput}
                  onChange={this.handleChange}
                />
              </div>
              <div className="w-100 w-third-ns w-25-l pl2-l mb3">
                <label htmlFor="dateOfBirth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">mm/dd/yyyy</span>
                </label>
                <input
                  id="dateOfBirth"
                  type="text"
                  className="w-100 pa3 br2 b--black-20"
                  aria-describedby={
                    this.state.invalidDate ? 'dob_msg' : undefined
                  }
                  aria-invalid={this.state.invalidDate}
                  onChange={this.handleChange}
                />
              </div>


              <div className="visually-hidden flex items-center pb1 mb3 ml3-ns ml0-l">
              { // TODO: The #-Results label and Remove buttons are "visually-hidden"
                // until Aliases feature is complete.
              }
                <span className="fw5 bl bw2 b--blue bg-gray-blue-2 pa2 pr3 mr2 mb2">1 Result</span>
                <button className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pa2 mb2">
                  <i aria-hidden={"true"} className="fas fa-times-circle pr1"></i>Remove
                </button>
              </div>
              </div>

              {
                // TODO: insert this when rendering additional Alias components.
                //<hr className="ba b--white mt0 mb3" />
              }

              <div className="flex">
              {  // Row containing The +Alias and search buttons.
              }
                <button className="visually-hidden w4 tc br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv3 ph3 mr2">
                {  // TODO: keep Alias button as "visually-hidden" until Aliases feature is complete.
                }
                  <i aria-hidden={"true"} className="fas fa-plus-circle pr1"></i>Alias

                </button>
                <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search"  type="submit">
                  <i aria-hidden="true" className="fas fa-search pr2"></i>
                  <span className="fw7">Search</span>
                </button>
              </div>

            <div role="alert" className="w-100">
              {this.state.missingInputs === true ? (
                <p id="name_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  First and last name are required.
                </p>
              ) : null}
              {this.state.invalidDate === true ? (
                <p id="dob_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  The date format must be MM/DD/YYYY.
                </p>
              ) : null}
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
