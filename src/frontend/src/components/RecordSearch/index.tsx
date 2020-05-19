import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { CaseData, RecordData } from './Record/types';
import {
  searchRecord,
  clearRecord
} from '../../redux/search/actions';
import SearchPanel from './SearchPanel';
import Record from './Record';
import Case from './Record/Case';
import Status from './Status';
import Header from '../Header';
import AddCaseButton from './Record/AddCaseButton';
import RecordSummary from './Record/RecordSummary';
import CaseEditPanel from './Record/CaseEditPanel';
import { checkOeciRedirect } from '../../service/cookie-service';

interface Props {
  searchRecord: Function;
  clearRecord: Function;
  record?: RecordData;
  dispositionWasUnknown?: string[];
};

interface State {
  addingNewCase: boolean;
}

class RecordSearch extends Component<Props, State> {
  state: State = {
    addingNewCase: false
  }
  componentDidMount() {
    checkOeciRedirect();
  }

  componentWillUnmount() {
    this.props.clearRecord();
  }

  blankCase : CaseData = {
    balance_due: 0,
    birth_year: 0,
    case_detail_link: "",
    case_number: "CASE-00X",
    charges: [],
    citation_number: "",
    current_status: "",
    date: "",
    location: "",
    name: "",
    violation_type: "",
  }
  render() {
    return (
      <>
      <Header/>
      <main className="mw8 center ph2">
        <SearchPanel searchRecord={this.props.searchRecord} />
        <Status/>
        {this.props.record && this.props.record.summary ? (
          <RecordSummary summary={this.props.record.summary}/>
          ) : null }

        {this.state.addingNewCase ?
          <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
            <Case dispositionWasUnknown={this.props.dispositionWasUnknown ? this.props.dispositionWasUnknown : [] } propogateState={()=>{this.setState({addingNewCase: false})}} case={this.blankCase} editing={true} isNewCase={true}/>
          </div> :
          <AddCaseButton onClick={()=>{this.setState({addingNewCase: true})}}/> }
        {this.props.record &&
        ((this.props.record.cases &&
        this.props.record.cases.length > 0) || this.props.record.errors) ? (
          <Record record={this.props.record} dispositionWasUnknown={this.props.dispositionWasUnknown ? this.props.dispositionWasUnknown : []} />
        ) : null}
        <div className="bg-white shadow mv4 pa4 br3">
          <h2 className="fw6 mb3">Assumptions</h2>
          <p className="mb3">We are only able to access your public Oregon records.</p>
          <p className="mb2">Your analysis may be different if you have had cases which were:</p>
          <ul className="lh-copy pl4 mw6 mb3">
            <li className="mb2">Previously expunged</li>
            <li className="mb2">From States besides Oregon within the last ten years</li>
            <li className="mb2">From Federal Court within the last ten years</li>
            <li className="mb2">From local District Courts, e.g. Medford Municipal Court (not Jackson County Circuit Court) from within the last ten years</li>
          </ul>
          <p>
            <a className="link hover-blue underline" href="/manual#assumption1">Learn more in the Manual</a>
          </p>
        </div>
      </main>
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    record: state.search.record,
    dispositionWasUnknown: state.search.dispositionWasUnknown
  };
};

export default connect(
  mapStateToProps,
  {
    searchRecord: searchRecord,
    clearRecord: clearRecord
  }
)(RecordSearch);
