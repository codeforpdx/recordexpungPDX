import React, { Component } from 'react';
import { connect } from 'react-redux';
import {
  loadSearchRecordsMockAction,
  loadSearchRecordsAction
} from '../redux/search-results/actions';

class AllSearchResults extends Component {
  componentDidMount() {
    console.log('helllo search results!');
    this.props.fetch();
  }

  render() {
    console.log('hi', this.props.fetch);
    return <h1>All Search and Results Container Place Holder</h1>;
  }
}
const mapDispatchToProps = dispatch => ({
  fetch() {
    //change loadSearchRecordsMockAction to loadSearchREcordsAction when get back end running
    return dispatch(loadSearchRecordsMockAction());
  }
});

export default connect(
  null,
  mapDispatchToProps
)(AllSearchResults);
