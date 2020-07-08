import React from "react";
import RecordSearch from "../../RecordSearch";
import { startDemo } from "../../../redux/search/actions";
import store from "../../../redux/store";

export default class Demo extends React.Component {
  componentDidMount() {
    store.dispatch(startDemo());
  }
  render() {
    return <RecordSearch demo={true} />;
  }
}
