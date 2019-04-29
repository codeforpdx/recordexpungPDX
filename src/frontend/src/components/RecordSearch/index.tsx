import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { loadRecords } from "../../redux/records/actions";

class RecordSearch extends React.Component {
  public render() {
    return <div/>;
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system,
});

export default connect(
  mapStateToProps,
  { loadRecords }
)(RecordSearch);