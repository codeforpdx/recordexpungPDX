import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { get } from 'lodash';
import { logOut } from "../../redux/system/actions";

class LogOut extends React.Component {

  constructor() {
    super(arguments[0]);
    this.logOutNow = this.logOutNow.bind(this);
  }

  public logOutNow() {
    // TODO: clean this up. Not yet sure how to appease Typescript here.
    get(this, 'props.logOut')();
    arguments[0].preventDefault();
    arguments[0].stopPropagation();
  }

  public render() {
    return(
      <span onClick={this.logOutNow}>
        {this.props.children}
      </span>
    )
  }

}

const mapStateToProps = (state: AppState) => ({
  system: state.system,
});

export default connect(
  mapStateToProps,
  { logOut }
)(LogOut);
