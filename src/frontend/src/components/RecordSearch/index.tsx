import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { loadRecords } from "../../redux/records/actions";
import moment from 'moment';

class RecordSearch extends React.Component {
  state = {
    firstName: null,
    lastName: null, // Null value ensures alerts are not present until form is submitted.
    dateOfBirth: '', // Moment expects a string to be passed in as a paramenter in the validateForm function.
    firstNameHasInput: false, // Initially set to false to ensure aria-invalid attribute is rendered.
    lastNameHasInput: false,
    missingInputs: null,
    invalidDate: false
  }

  handleChange = (e: React.BaseSyntheticEvent) => {
    this.setState({
      [e.target.id]: e.target.value
    });
  }

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm();
    if (this.state.missingInputs === false && this.state.invalidDate === false) {
      // Dispatch an action.
    };
  }

  validateForm = () => {
    this.setState({firstNameHasInput: !this.state.firstName});
    this.setState({lastNameHasInput: !this.state.lastName});
    this.setState({missingInputs: !this.state.firstName || !this.state.lastName || !this.state.dateOfBirth});
    this.setState({invalidDate: moment(this.state.dateOfBirth, 'MM/DD/YYYY', true).isValid() === false});
  }

  public render() {
    return (
      <main className='mw8 center ph2'>
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
                  aria-invalid={this.state.firstNameHasInput}
                  onChange={this.handleChange}/>
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
                  aria-invalid={this.state.lastNameHasInput}
                  onChange={this.handleChange}/>
              </div>
              <div className="w-100 w-30-ns mb3 pr2-ns">
                <label htmlFor="dateOfBirth" className="db mb1 fw6">
                  Date of Birth <span id="dob_msg"className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input
                  id="dateOfBirth"
                  type="text"
                  className="w-100 pa3 br2 b--black-20"
                  required
                  aria-describedby="dob_msg"
                  aria-invalid={this.state.invalidDate}
                  onChange={this.handleChange}/>
              </div>
              <div className="w-100 w-10-ns mb3">
                <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search" type="submit">
                  <span className="visually-hidden">Search Records</span>
                  <i aria-hidden="true" className="fas fa-search"></i>
                </button>
              </div>
              <div role="alert" className="w-100">
                {this.state.missingInputs === true ? <p className="bg-washed-red mv4 pa3 br3 fw6">All search fields are required.</p> : null}
                {this.state.invalidDate === true ? <p className="bg-washed-red mv4 pa3 br3 fw6">The date format must be MM/DD/YYYY.</p> : null}
              </div>
            </div>
          </form>
        </section>
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system,
});

export default connect(
  mapStateToProps,
  { loadRecords }
)(RecordSearch);
