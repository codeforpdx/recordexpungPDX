import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/records/types';
import { loadSearchRecordsMock } from '../redux/records/mock-actions';
import RecordSearch from '../components/RecordSearch';

type Props = {
  fetch: Function;
  records: Record[];
};

class AllRecords extends Component<Props> {
  componentDidMount() {
    this.props.fetch();
    //Next we need to pass down the fetch to RecordSearch component as a prop, and trigger it
    //on a new search instead of componentDidMount.  When this happens we shoud replace the loadSearchRecordsMock function with a real api call
    //and use the populated fields in the RecrodSearch component as paramaters for the API request.
  }

  render() {
    // We still need to create and import SeachResults component and pass it records down as a prop so that it can render new records
    // This component should be rendered below the <RecordSearch /> coponent below.
    return (
      <>
        <RecordSearch />
      </>
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
    fetch: loadSearchRecordsMock
  }
)(AllRecords);
