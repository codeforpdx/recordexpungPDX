import React, { Component } from 'react';
import { connect } from 'react-redux';
import {
  loadSearchRecordsMockAction,
  loadSearchRecordsAction
} from '../redux/search-results/actions';

type Props = {
  fetch: Function;
};

class AllSearchResults extends Component<Props> {
  componentDidMount() {
    console.log('helllo search results!');
    this.props.fetch();
  }

  render() {
    return <h1>All Search and Results Container Place Holder</h1>;
  }
}
const mapDispatchToProps = (dispatch: Function) => ({
  fetch() {
    //change loadSearchRecordsMockAction to loadSearchRecordsAction when get back end running
    return dispatch(loadSearchRecordsMockAction());
  }
});

export default connect(
  null,
  mapDispatchToProps
)(AllSearchResults);
