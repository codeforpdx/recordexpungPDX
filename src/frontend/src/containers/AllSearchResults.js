import React, { Component } from 'react';
import { connect } from 'react-redux';
import { loadSearchRecords } from '../redux/search-results/actions';

class AllSearchResults extends Component {
  componentDidMount() {
    console.log('helllo search results!');
    this.props.fetch();
  }

  render() {
    console.log('hi');
    return <h1>All Search and Results Container Place Holder</h1>;
  }
}
const mapDispatchToProps = dispatch => ({
  async fetch() {
    return await dispatch(loadSearchRecords());
  }
});

export default connect(
  null,
  mapDispatchToProps
)(AllSearchResults);
