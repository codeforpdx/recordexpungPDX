import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { refreshLocalAuth } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import { decodeCookie } from '../../service/cookie-service';

interface Props {
  refreshLocalAuth: typeof refreshLocalAuth;
  system: SystemState;
}

interface State {
  loading: boolean;
}

class Authenticator extends React.Component<Props> {
  public state: State = {
    loading: true
  };

  public componentDidMount() {
    const cookieData = decodeCookie();
    if (cookieData.remember_token) {
      this.props.refreshLocalAuth();
    }
    this.setState({
      loading: false
    });
  }

  public render() {
    return this.state.loading ? null : this.props.children;
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  { refreshLocalAuth }
)(Authenticator);
