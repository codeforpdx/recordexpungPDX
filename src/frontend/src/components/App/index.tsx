import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { SystemState } from '../../redux/system/types';
import { Router, Route, Switch } from 'react-router-dom';
import { refreshLocalAuth } from '../../redux/system/actions';

import history from '../../service/history';
import Footer from '../Footer';
import LogIn from '../LogIn';
import LoggedInHeader from '../LoggedInHeader';
import RecordSearch from '../RecordSearch';
import OeciLogin from '../OeciLogin';
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';
import Admin from '../Admin';
import AuthenticatedRoute from '../AuthenticatedRoute';
import PublicRoute from '../PublicRoute';
import InterimPage from '../InterimPage';

interface Props {
  refreshLocalAuth: typeof refreshLocalAuth;
  system: SystemState;
}

interface State {
  loading: boolean;
}

class App extends React.Component<Props> {
  public state: State = {
    loading: true
  };

  public componentDidMount() {
    const data: any = document.cookie.split(';').reduce((res, c) => {
      const [key, val] = c
        .trim()
        .split('=')
        .map(decodeURIComponent);
      const allNumbers = (str: string) => /^\d+$/.test(str);
      try {
        return Object.assign(res, {
          [key]: allNumbers(val) ? val : JSON.parse(val)
        });
      } catch (e) {
        return Object.assign(res, { [key]: val });
      }
    }, {});
    if (data.authToken.length > 0 || data.userId.length > 0) {
      this.props.refreshLocalAuth(data.authToken, data.userId);
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
      <Router history={history}>
        {this.displayHeader()}
        <Switch>
          <AuthenticatedRoute
            path="/oeci"
            component={OeciLogin}
            isAuthenticated={this.props.system.loggedIn}
          />
          <AuthenticatedRoute
            path="/record-search"
            component={RecordSearch}
            isAuthenticated={this.props.system.loggedIn}
          />
          <AuthenticatedRoute
            path="/stats"
            component={InterimPage}
            isAuthenticated={this.props.system.loggedIn}
          />
          <AuthenticatedRoute
            path="/admin"
            component={Admin}
            isAuthenticated={this.props.system.loggedIn}
          />
          <AuthenticatedRoute
            path="/account"
            component={InterimPage}
            isAuthenticated={this.props.system.loggedIn}
          />
          <PublicRoute
            exact
            path="/"
            component={LogIn}
            isAuthenticated={this.props.system.loggedIn}
          />
          {/* <Route exact={true} path="/">
            {!this.props.system.loggedIn && <LogIn/>}
          </Route> */}
          <PublicRoute
            path="/forgot-password"
            component={ForgotPassword}
            isAuthenticated={this.props.system.loggedIn}
          />
          <PublicRoute
            path="/password-reset"
            component={PasswordReset}
            isAuthenticated={this.props.system.loggedIn}
          />
        </Switch>
        <Footer />
      </Router>
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
