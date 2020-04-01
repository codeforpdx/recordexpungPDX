import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/records/types';
import {
  loadSearchRecords,
  clearSearchRecords
} from '../redux/records/actions';
import RecordSearch from '../components/RecordSearch';
import SearchResults from '../components/SearchResults';
import AllStatus from './AllStatus';
import { checkOeciRedirect } from '../service/cookie-service';

type Props = {
  fetchRecords: Function;
  clearRecords: Function;
  record?: Record;
};

class AllRecords extends Component<Props> {
  componentWillMount() {
    checkOeciRedirect();
  }

  componentWillUnmount() {
    this.props.clearRecords();
  }

  render() {
    // Once fetch adds records to Redux, a SearchResults container is rendered with updated records
    return (
      <main className="mw8 center ph2">
        <RecordSearch fetchRecords={this.props.fetchRecords} />
        {this.props.record &&
        ((this.props.record.cases &&
        this.props.record.cases.length > 0) || this.props.record.errors) ? (
          <SearchResults record={this.props.record} />
        ) : (
          <AllStatus />
        )}
        <div className="bg-white shadow mv4 pa4 br3">
          <h2 className="fw6 mb3">Assumptions</h2>
          <p className="mb3">We are only able to access your public Oregon records.</p>
          <p className="mb2">Your analysis may be different if you have had cases which were:</p>
          <ul className="lh-copy pl4 mw6">
            <li className="mb2">Previously expunged</li>
            <li className="mb2">From States besides Oregon within the last ten years</li>
            <li className="mb2">From Federal Court within the last ten years</li>
            <li className="mb2">From local District Courts, e.g. Medford Municipal Court (not Jackson County Circuit Court) from within the last ten years</li>
          </ul>
        </div>
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    record: state.records.records
  };
};

export default connect(
  mapStateToProps,
  {
    fetchRecords: loadSearchRecords,
    clearRecords: clearSearchRecords
  }
)(AllRecords);
