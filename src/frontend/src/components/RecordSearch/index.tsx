import React, { Component } from "react";
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { RecordData } from "./Record/types";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import DemoInfo from "./Demo/DemoInfo";
import { checkOeciRedirect } from "../../service/cookie-service";
import { Link } from "react-router-dom";

interface Props {
  demo: boolean;
  record?: RecordData;
}

class RecordSearch extends Component<Props> {
  componentDidMount() {
    this.props.demo || checkOeciRedirect();
  }

  render() {
    return (
      <>
        <main className="mw8 center f6 f5-l ph2">
          {this.props.demo && <DemoInfo />}
          <SearchPanel />
          <Status record={this.props.record} />
          <Record record={this.props.record} />
          <div className="bg-white shadow mb6 pa4 br3">
            <h2 className="fw6 mb3">Assumptions</h2>
            <p className="mb3">
              We are only able to access your public Oregon records.
            </p>
            <p className="mb2">
              Your analysis may be different if you have had cases which were:
            </p>
            <ul className="lh-copy pl4 mw6 mb3">
              <li className="mb2">Previously expunged</li>
              <li className="mb2">
                From States besides Oregon within the last ten years
              </li>
              <li className="mb2">
                From Federal Court within the last ten years
              </li>
              <li className="mb2">
                From local District Courts, e.g. Medford Municipal Court (not
                Jackson County Circuit Court) from within the last ten years
              </li>
            </ul>
            <p>
              <Link
                className="link hover-blue underline"
                to="/manual#assumption1"
                onClick={() => window.scrollTo(0, 0)}
              >
                Learn more in the Manual
              </Link>
            </p>
          </div>
        </main>
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    record: state.search.record,
  };
};

export default connect(mapStateToProps, {})(RecordSearch);
