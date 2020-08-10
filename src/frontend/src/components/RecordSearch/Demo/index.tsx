import React from "react";
import RecordSearch from "../../RecordSearch";
import { startDemo } from "../../../redux/search/actions";
import store from "../../../redux/store";
import { connect } from "react-redux";

interface Props {
  startDemo: Function;
}
class Demo extends React.Component<Props> {
  componentDidMount() {
    store.dispatch(this.props.startDemo());
  }
  render() {
    return <RecordSearch />;
  }
}

export default connect(() => {}, { startDemo })(Demo);
