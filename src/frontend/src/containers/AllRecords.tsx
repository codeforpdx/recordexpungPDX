import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/records/types';
import { loadSearchRecordsMock } from '../redux/records/mock-actions';

type Props = {
  fetch: Function;
  records: Record[];
};

class AllRecords extends Component<Props> {
  componentDidMount() {
    this.props.fetch();
    //When we render the search component, fetch should be passed down to it as a prop.
  }
  render() {
    // ***NOTE***
    // Eventually the search and searchResults component will replace the button that is currently rendered.
    // When this happens fetch will be passed down  to the search componen as a prop and invoked when user searches for records.
    // The records will then be passed to Redux and passed down as props to searchResults component.
    return <></>;
  }
}

const mapStateToProps = (state: AppState) => {
  console.log(state.records);
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
