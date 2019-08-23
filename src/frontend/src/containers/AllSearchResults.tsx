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
  public log(event: React.SyntheticEvent) {
    console.log(this.props.fetch);
  }

  records = () => {
    console.log(this.props.records);
  };

  componentDidMount() {
    console.log('helllo search results!');
    this.props.fetch();
  }

  render() {
    //Now that the records is available in props, you can render
    //the SearchResultsComponent and pass it the records as a prop
    //<SearchResultsComponent records={this.props.records}>
    //Currently you can now hit the button and console log the records
    //that were fetched from redux
    return <button onClick={this.records}>Console Log Current Props</button>;
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
