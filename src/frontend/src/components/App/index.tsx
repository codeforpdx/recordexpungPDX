import React from 'react';
import { connect } from 'react-redux';
import { get } from 'lodash';
import { AppState } from '../../redux/store';
import { Router, Route } from 'react-router-dom';

import history from '../History';
import Footer from '../Footer';
import LogIn from '../LogIn';
import LoggedIn from '../LoggedIn';
import RecordSearch from '../RecordSearch';
import OeciLogin from '../OeciLogin';
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';
import Admin from '../Admin';

class App extends React.Component {
  public render() {
    return get(this, 'props.system.loggedIn') ? (
      <Router history={history}>
        <LoggedIn>
          <Route path="/oeci" component={OeciLogin} />
          <Route path="/record-search" component={RecordSearch} />
          <Route path="/stats" /*component={}*/ />
          <Route path="/admin" component={Admin} />
          <Route path="/account" /*component={}*/ />
        </LoggedIn>
      </Router>
    ) : (
      <Router history={history}>
        <Route exact path="/" component={LogIn} />
        <Route exact path="/" component={Footer} />
        <Route path="/forgot-password" component={ForgotPassword} />
        <Route path="/password-reset" component={PasswordReset} />
      </Router>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  {}
)(App);
