import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import { Record } from '../redux/types';
import {
  loadSearchRecordsMock,
  loadSearchRecords
} from '../redux/search-results/actions';

type Props = {
  loadSearchRecords: Function;
  loadSearchRecordsMock: Function;
  records: Record[];
};

class AllSearchResults extends Component<Props> {
  componentDidMount() {
    //switch to loadSearchRecordsAction when go to production
    // this.props.dispatch(loadSearchRecordsMockAction())
    // loadSearchRecordsMockActionNotThunk(this.props.dispatch)
    this.props.loadSearchRecordsMock();
  }
  render() {
    //actions vs action creators
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
    console.log('props', this.props);
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

const mapDispatchToProps = {
  loadSearchRecordsMock,
  loadSearchRecords
};

const mapStateToProps = (state: AppState) => ({
  records: state.searchRecordsReducer.records
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AllSearchResults);
