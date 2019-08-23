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

  thingy = () => {
    console.log(this.props);
  };

  componentDidMount() {
    console.log('helllo search results!');
    this.props.fetch();
  }

  render() {
    return <button onClick={this.thingy}>log</button>;
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
