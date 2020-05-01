import React from 'react';
import {answerDisposition} from '../../../redux/search/actions';
import {connect} from 'react-redux';
import store from '../../../redux/store';
import moment from 'moment';

interface Props {
  case_number: string;
  ambiguous_charge_id: string;
  disposition: any;
}

interface State {
  status: string;
  conviction_date: string;
  probation_revoked_date: string;
  missingFields: boolean;
  invalidDate: boolean
}

export default class DispositionQuestion extends React.Component<Props, State> {

  state: State  = {
    status: "Open",
    conviction_date: "",
    probation_revoked_date: "",
    missingFields: false,
    invalidDate: false
  }
  componentDidMount() {
    this.setState({
      status: (this.props.disposition ? this.props.disposition.status : "Open") ,
      conviction_date: (this.props.disposition ? this.props.disposition.date : ""),
      }
    )
  }

  handleChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      [e.target.name]: e.target.value
    });
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then( () => {
      if (!this.state.missingFields  && !this.state.invalidDate) {
        store.dispatch(
          answerDisposition(
            this.props.case_number,
            this.props.ambiguous_charge_id,
            this.state.status,
            (this.state.status === "Convicted" || this.state.status === "revoked" ? this.state.conviction_date : "1/1/2020"), // The date for a dismissal doesn't matter, but the backend expects something so here we are.
             this.state.probation_revoked_date)
        )
      }
    })
  };

  validateForm = () => {
    return new Promise(resolve => {
      let missingFields = false;
      if (this.state.status === "Convicted") {
        missingFields = this.state.conviction_date === "";
      } else if (this.state.status === "revoked") {
        missingFields = this.state.conviction_date === "" || this.state.probation_revoked_date === "";
      }

      let invalidDate = ( this.state.status === "Convicted" || this.state.status === "revoked") &&
        (this.state.conviction_date.length !== 0 && !moment(this.state.conviction_date, 'M/D/YYYY', true).isValid()) ||
        (this.state.probation_revoked_date.length !== 0 && !moment(this.state.probation_revoked_date, 'M/D/YYYY', true).isValid())
      ;
      this.setState(
        {
          missingFields: missingFields ,
          invalidDate: invalidDate
        },
      resolve
      );
    });
  };

  render() {
    return (
      <form className="w-100 bt bw3 b--light-purple pa3 pb1" onSubmit={this.handleSubmit}>
        <fieldset className="relative mb4">
            <legend className="fw7 mb2">What is the disposition?</legend>
            {"props: " + JSON.stringify(this.props)}
            {"state: " + JSON.stringify(this.state)}
            <div className="radio">
                <div className="dib">
                    <input id="dis" name="status" type="radio" value="Dismissed" checked={this.state.status==="Dismissed"} onChange={this.handleChange} />
                    <label htmlFor="dis">Dismissed</label>
                </div>
                <div className="dib">
                    <input id="con" name="status" type="radio" value="Convicted" checked={this.state.status==="Convicted"} onChange={this.handleChange} />
                    <label htmlFor="con">Convicted</label>
                </div>
                <div className="dib">
                    <input id="rev" name="status" type="radio" value="revoked" checked={this.state.status==="revoked"} onChange={this.handleChange} />
                    <label htmlFor="rev">Probation Revoked</label>
                </div>
                <div className="dib">
                    <input id="open" name="status" type="radio" value="Open" checked={this.state && this.state.status==="Open"} onChange={this.handleChange} />
                    <label htmlFor="open">Open</label>
                </div>
            </div>
            <div className={this.state && (this.state.status === "Convicted" || this.state.status === "revoked") ? "" : "visually-hidden"}>
              <label className="db fw6 mt3 mb1" htmlFor="n">Date Convicted <span className="f6 fw4">mm/dd/yyyy</span></label>
              <input onChange={this.handleChange} className="w5 br2 b--black-20 pa3" id="n" type="text" name="conviction_date"/>
            </div>
            <div className={this.state && this.state.status === "revoked" ? "" : "visually-hidden"}>
              <label className="db fw6 mt3 mb1" htmlFor="n">Date Probation Revoked <span className="f6 fw4">mm/dd/yyyy</span></label>
              <input onChange={this.handleChange} className="w5 br2 b--black-20 pa3" id="n" type="text" name="probation_revoked_date"/>
            </div>
            <button className="db bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 mt3">Submit</button>
            <div role="alert">
              <p className={(this.state && this.state.missingFields ? "" : "visually-hidden " ) + "dib bg-washed-red fw6 br3 pa3 mt3"}>Please complete all fields</p>
            </div>
            <div role="alert">
              <p className={(this.state && this.state.invalidDate ? "" : "visually-hidden " ) + "dib bg-washed-red fw6 br3 pa3 mt3"}>The date format must be MM/DD/YYYY</p>
            </div>

        </fieldset>
      </form>
    )
  }
}
