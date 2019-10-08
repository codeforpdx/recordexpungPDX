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
    // Upon page refresh or navigation via manual url input this will
    // repopulate store with information stored in the browser cookie
    const cookieData = decodeCookie();
    if (cookieData.authToken && cookieData.userId) {
      this.props.refreshLocalAuth(cookieData.authToken, cookieData.userId);
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
