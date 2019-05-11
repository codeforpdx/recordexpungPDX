import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { loadRecords } from "../../redux/records/actions";


// This is a placeholder component. I created it to prototype
// out the general structure we'll need when working with
// Records using Redux.

class RecordSearch extends React.Component {
  state = {
    firstName: null,
    lastName: null,
    dateOfBirth: null
  }
  //not sure what the correct typing is here
  handleChange = (e: any ) => {
    console.log(e)
      this.setState({
        [e.target.id]:e.target.value
      })
  }
  
  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(this.state);
  }

  public render() {
    return (
      <main className='mw8 center ph2'>
        <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
          <h1 className="mb4 f4 fw6">Record Search</h1>
          <form onSubmit={this.handleSubmit}>
            <div className="flex flex-wrap items-end">
              <div className="w-100 w-30-ns mb3 pr2-ns">
                <label htmlFor="firstName" className="db mb1 fw6">
                  First Name
                </label>
                <input
                  id="firstName"
                  type="text"
                  className="w-100 pa3 br2 b--black-20"

                  aria-invalid="false"
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

                  aria-invalid="false"
                  onChange={this.handleChange}/>
              </div>
              <div className="w-100 w-30-ns mb3 pr2-ns">
                <label htmlFor="dateOfBirth" className="db mb1 fw6">
                  Date of Birth <span className="fw2 f6">MM/DD/YYYY</span>
                </label>
                <input
                  id="dateOfBirth"
                  type="text"
                  className="w-100 pa3 br2 b--black-20"

                  aria-describedby="dob_msg"
                  aria-invalid="false"
                  onChange={this.handleChange}/>
              </div>
              <div className="w-100 w-10-ns mb3">
                <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search" type="submit">
                  <span className="visually-hidden">Search Records</span>
                  <i aria-hidden="true" className="fas fa-search"></i>
                </button>
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
