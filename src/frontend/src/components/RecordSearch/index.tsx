import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { loadRecords } from "../../redux/records/actions";

// This is a placeholder component. I created it to prototype
// out the general structure we'll need when working with
// Records using Redux.

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
