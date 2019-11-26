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
  records?: Record;
};

class AllRecords extends Component<Props> {
  componentWillMount() {
    checkOeciRedirect();
  }

  componentWillUnmount() {
    this.props.clearRecords();
  }

  render() {
    // Fetch has now been passed down to RecordSearch component and is triggered when submit button is pressed.
    // Currently no matter what the user puts in the search fields, it still triggers a mock fetch with pre determined API response
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
    fetchRecords: loadSearchRecords,
    clearRecords: clearSearchRecords
  }
)(AllRecords);
