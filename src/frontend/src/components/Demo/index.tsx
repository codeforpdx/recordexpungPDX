import React from "react";
import { connect } from "react-redux";
import { RecordData } from "../RecordSearch/Record/types";
import store, { AppState } from "../../redux/store";
import { startDemo } from "../../redux/search/actions";
import DemoInfo from "./DemoInfo";
import SearchPanel from "../RecordSearch/SearchPanel";
import Status from "../RecordSearch/Status";
import Record from "../RecordSearch/Record";
import Assumptions from "../RecordSearch/Assumptions";

interface Props {
  record?: RecordData;
  startDemo: Function;
}

class Demo extends React.Component<Props> {
  componentDidMount() {
    document.title = "Demo - RecordSponge";
    store.dispatch(this.props.startDemo());
  }

  render() {
    return (
      <main className="mw8 center f6 f5-l ph2">
        <DemoInfo />
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

export default connect(mapStateToProps, { startDemo })(Demo);
