import React from "react";
import { connect } from "react-redux";
import { RecordData } from "./Record/types";
import store, { AppState } from "../../redux/store";
import { stopDemo } from "../../redux/search/actions";
import { checkOeciRedirect } from "../../service/cookie-service";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import Assumptions from "./Assumptions";

interface Props {
  record?: RecordData;
  stopDemo: Function;
}

class RecordSearch extends React.Component<Props> {
  componentDidMount() {
    checkOeciRedirect();
    document.title = "Search Records - RecordSponge";
    store.dispatch(this.props.stopDemo());
  }

  render() {
    return (
      <main className="mw8 center f6 f5-l ph2">
        <SearchPanel />
        <Status record={this.props.record} />
        <Record record={this.props.record} />
        <Assumptions />
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    record: state.search.record,
  };
};

export default connect(mapStateToProps, { stopDemo })(RecordSearch);
