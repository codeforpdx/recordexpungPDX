import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/types';
import {
  loadSearchRecordsMockAction,
  loadSearchRecordsAction
} from '../redux/search-results/actions';

type Props = {
  fetch: Function;
  records: Record[];
};

class AllSearchResults extends Component<Props> {
  componentDidMount() {
    this.props.fetch();
  }
  render() {
    //NOTE 1*****
    //Now that the records array available in props, you can render
    //the SearchResultsComponent and pass it the records as a prop
    //<SearchResultsComponent records={this.props.records}>
    //Currently you can now hit the rendered button and console log the records
    //that were fetched from redux
    //NOTE 2****
    //The RecordSearch Component should be imported and rendered here.
    //fetch should be passed down to the RecordSearchComponent and invoked
    //when a search has been performed.

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
const mapDispatchToProps = (dispatch: Function) => ({
  fetch() {
    //change loadSearchRecordsMockAction to loadSearchRecordsAction when get back end running
    return dispatch(loadSearchRecordsMockAction());
  }
});

const mapStateToProps = (state: AppState) => ({
  records: state.searchRecordsReducer.search_records
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AllSearchResults);
