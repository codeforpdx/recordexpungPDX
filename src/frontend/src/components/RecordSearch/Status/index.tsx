import React from "react";
import { connect } from "react-redux";
import { AppState } from "../../../redux/store";
import { RecordData } from "../Record/types";
import LoadingSpinner from "../../LoadingSpinner";
import NoSearchResults from "./NoSearchResults";

type Props = {
  loading: string;
  record?: RecordData;
};

class Status extends React.Component<Props> {
  render() {
    const empty_record = this.props.record &&
      this.props.record.cases && this.props.record.cases.length === 0
    return (
      <section>
        {this.props.loading === "loading" ? (
          <LoadingSpinner inputString={"your search results"} />
        ) : (
          empty_record ? (
            <NoSearchResults />
          ) : (
            null
          )
        )}
      </section>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    loading: state.search.loading,
  };
};

export default connect(mapStateToProps)(Status);
