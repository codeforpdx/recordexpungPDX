import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { SystemState } from '../../redux/system/types';
import { refreshLocalAuth } from '../../redux/system/actions';
import AppRouter from '../AppRouter';
import LoggedInHeader from '../LoggedInHeader';
import Footer from '../Footer';
import { decodeCookie } from '../../service/cookie-service';

interface Props {
  refreshLocalAuth: typeof refreshLocalAuth;
  system: SystemState;
}

interface State {
  loading: boolean;
}

interface CookieData {
  authToken: string;
  userId: string;
}

class App extends React.Component<Props> {
  public state: State = {
    loading: true
  };

  public componentDidMount() {
    // Upon page refresh or navigation via manual url input this will
    // repopulate store with information stored in the browser cookie
    const cookieData: CookieData = decodeCookie();
    if (cookieData.authToken || cookieData.userId) {
      this.props.refreshLocalAuth(cookieData.authToken, cookieData.userId);
    }
    this.setState({
      loading: false
    });
  }

  public displayHeader = () => {
    return this.props.system.loggedIn ? <LoggedInHeader /> : null;
  };

  public displayApp = () => {
    return this.state.loading ? null : (
      <>
        {this.displayHeader()}
        <AppRouter />
        <Footer />
      </>
    );
  };

  public render() {
    return this.displayApp();
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  { refreshLocalAuth }
)(App);
