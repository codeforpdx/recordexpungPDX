import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/records/types';
import { loadSearchRecordsMock } from '../redux/records/mock-actions';
import RecordSearch from '../components/RecordSearch';
import SearchResults from '../components/SearchResults';
import AllStatus from './AllStatus';

type Props = {
  fetchRecords: Function;
  records?: Record;
};

class AllRecords extends Component<Props> {
  render() {
    // Fetch has now been passed down to RecordSearch componant and is triggered when submit button is pressed.
    // Currentlly no matter what the user puts in the search fields, it still triggers a mock fetch with pre determined API response
    // Once fetch adds records to Redux, a SearchResults container is rendered with updated records
    return (
      <main className="mw8 center ph2">
        <RecordSearch fetchRecords={this.props.fetchRecords} />
        {this.props.records ? (
          <SearchResults records={this.props.records} />
        ) : (
          <AllStatus />
        )}
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    records: state.records.records
  };
};

export default connect(
  mapStateToProps,
  {
    fetchRecords: loadSearchRecordsMock
  }
)(AllRecords);
