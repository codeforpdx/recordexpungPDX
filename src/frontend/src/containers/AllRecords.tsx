import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/records/types';
import { loadSearchRecords } from '../redux/records/actions';
import { loadSearchRecordsMock } from '../redux/records/mock-actions';

type Props = {
  fetch: Function;
  records: Record[];
};

class AllSearchResults extends Component<Props> {
  componentDidMount() {
    this.props.fetch();
    //When we render the search component, fetch should be passed down to it as a prop.
  }
  render() {
    // ***NOTE***
    // Eventually the search and searchResults component will replace the button that is currently rendered.
    // When this happens fetch will be passed down  to the search componen as a prop and invoked when user searches for records.
    // The records will then be passed to Redux and passed down as props to searchResults component.
    return (
      <button
        onClick={() => {
          console.log(this.props.records);
        }}
      >
        Console Log Current Records
      </button>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  records: state.searchRecordsReducer.records
});

export default connect(
  mapStateToProps,
  {
    //switch fetch: loadSearchRecordsMock to fetch: loadSearchRecords when connect to back end
    fetch: loadSearchRecordsMock
  }
)(AllSearchResults);
