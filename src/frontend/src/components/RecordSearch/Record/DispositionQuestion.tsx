import React from 'react';
import {answerDisposition} from '../../../redux/search/actions';
import {connect} from 'react-redux';
import store, {AppState} from '../../../redux/store';
import moment from 'moment';

interface Props {
  case_number: string;
  ambiguous_charge_id: string;
  disposition: any;
  loading?: boolean;
}

interface State {
  status: string;
  conviction_date: string;
  probation_revoked_date: string;
  missingFields: boolean;
  invalidDate: boolean;
  submitClickPending: boolean;
}

class DispositionQuestion extends React.Component<Props, State> {
  state: State  = {
    status: "Unknown",
    conviction_date: "",
    probation_revoked_date: "",
    missingFields: false,
    invalidDate: false,
    submitClickPending: false
  };

  componentDidMount() {
    this.setState({
      status: this.props.disposition.status,
      conviction_date: (this.props.disposition ? this.props.disposition.date : ""),
      }
    )
  }

  handleDismissedClick = () => {
    this.setState<any>({
      status: "Dismissed",
      conviction_date: "",
      probation_revoked_date: "",
      missingFields: false,
      invalidDate: false,
      submitClickPending: false
    }, this.dispatchAnswer);
  };

  handleConvictedClick = () => {
    this.setState<any>({
      status: "Convicted",
      probation_revoked_date: "",
      missingFields: false,
      invalidDate: false,
      submitClickPending: true
    });
  };

  handleRevokedClick = () => {
    this.setState<any>({
      status: "revoked",
      submitClickPending : true
    });
  };

  handleUnknownClick = () => {
    this.setState<any>({
      status: "Unknown",
      submitClickPending: false,
      conviction_date: "",
      probation_revoked_date: "",
      missingFields: false,
      invalidDate: false
    }, this.dispatchAnswer);
  };

  handleDateFieldChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      submitClickPending: true,
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then(() => {
      if (!this.state.missingFields && !this.state.invalidDate) {
        this.setState<any>({
          submitClickPending : false
        });
        this.dispatchAnswer();
      }
    });
  };

  dispatchAnswer = () => {
    store.dispatch(
      answerDisposition(
        this.props.case_number,
        this.props.ambiguous_charge_id,
        this.state.status,
        this.state.conviction_date || "1/1/2020", // The date for a dismissal doesn't matter, but the backend expects something so here we are.
        this.state.probation_revoked_date
      )
    )
  };

  validateForm = () => {
    return new Promise(resolve => {
      let missingFields = false;
      if (this.state.status === "Convicted") {
        missingFields = this.state.conviction_date === "";
      } else if (this.state.status === "revoked") {
        missingFields = this.state.conviction_date === "" || this.state.probation_revoked_date === "";
      }

      let invalidDate = (this.state.status === "Convicted" || this.state.status === "revoked") &&
        (this.state.conviction_date.length !== 0 && !moment(this.state.conviction_date, 'M/D/YYYY', true).isValid()) ||
        (this.state.probation_revoked_date.length !== 0 && !moment(this.state.probation_revoked_date, 'M/D/YYYY', true).isValid());
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
      <form className="w-100 bl bw3 b--light-purple pa3 pb1" onSubmit={this.handleSubmit}>
        <fieldset className="relative mb4">
            <legend className="fw7 mb2">Choose a disposition</legend>
            <div className="radio">
                <div className="dib">
                    <input id={this.props.ambiguous_charge_id + "-dis"} name="status" type="radio" value="Dismissed" checked={this.state.status==="Dismissed"} onChange={this.handleDismissedClick} />
                    <label htmlFor={this.props.ambiguous_charge_id + "-dis"}>Dismissed</label>
                </div>
                <div className="dib">
                    <input id={this.props.ambiguous_charge_id + "-con"} name="status" type="radio" value="Convicted" checked={this.state.status==="Convicted"} onChange={this.handleConvictedClick} />
                    <label htmlFor={this.props.ambiguous_charge_id + "-con"}>Convicted</label>
                </div>
                <div className="dib">
                    <input id={this.props.ambiguous_charge_id + "-rev"} name="status" type="radio" value="revoked" checked={this.state.status==="revoked"} onChange={this.handleRevokedClick} />
                    <label htmlFor={this.props.ambiguous_charge_id + "-rev"}>Probation Revoked</label>
                </div>
                <div className="dib">
                    <input id={this.props.ambiguous_charge_id + "-unknown"} name="status" type="radio" value="Unknown" checked={this.state && this.state.status==="Unknown"} onChange={this.handleUnknownClick} />
                    <label htmlFor={this.props.ambiguous_charge_id + "-unknown"}>Unknown</label>
                </div>
            </div>
            <div className={this.state && (this.state.status === "Convicted" || this.state.status === "revoked") ? "" : "visually-hidden"}>
              <label className="db fw6 mt3 mb1" htmlFor="n">Date Convicted <span className="f6 fw4">mm/dd/yyyy</span></label>
              <input value={this.state.conviction_date} onChange={this.handleDateFieldChange} className="w5 br2 b--black-20 pa3" id="n" type="text" name="conviction_date"/>
            </div>
            <div className={this.state && this.state.status === "revoked" ? "" : "visually-hidden"}>
              <label className="db fw6 mt3 mb1" htmlFor="n">Date Probation Revoked <span className="f6 fw4">mm/dd/yyyy</span></label>
              <input value={this.state.probation_revoked_date} onChange={this.handleDateFieldChange} className="w5 br2 b--black-20 pa3" id="n" type="text" name="probation_revoked_date"/>
            </div>
            {
              this.state.submitClickPending ?
                <button className="db bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 mt3">Submit</button> :
                null
            }
            {
              this.props.loading ?
                <div className="radio-spinner absolute" role="status">
                  <span className="spinner spinner--sm mr1"></span>
                  <span className="f6 fw5">Updating&#8230;</span>
                </div> :
                null
            }
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

function mapStateToProps(state: AppState, ownProps: Props) {
  return {
      case_number: ownProps.case_number,
      ambiguous_charge_id: ownProps.ambiguous_charge_id,
      disposition: ownProps.disposition,
      loading: state.search.loading
    };

}

export default connect(
  mapStateToProps,
  {
  }
)(DispositionQuestion);
