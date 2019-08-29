import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { logOut } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';

interface Props {
  system: SystemState;
  logOut: typeof logOut;
}

interface State {}

class LogOut extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.logOutNow = this.logOutNow.bind(this);
  }

  public logOutNow(event: React.SyntheticEvent) {
    this.props.logOut();
    event.preventDefault();
    event.stopPropagation();
  }

  public render() {
    return <span onClick={this.logOutNow}>{this.props.children}</span>;
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  { logOut }
)(LogOut);
