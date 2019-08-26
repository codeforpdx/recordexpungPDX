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
<<<<<<< 685562e274f71eefd6f70618532dcb8cbe40a04f
import OeciLogin from '../OeciLogin';
=======
import OeciLogin from '../OECI';
>>>>>>> heroku deploy file structure still in progress
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';

class App extends React.Component {
  public render() {
    return get(this, 'props.system.loggedIn') ? (
      <Router history={history}>
        <LoggedIn>
          <Route path="/oeci" component={OeciLogin} />
          <Route path="/record-search" component={RecordSearch} />
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
