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
import OECIlogin from '../OECI';
import ForgotPassword from '../ForgotPassword';

class App extends React.Component {
  public render() {
    return get(this, 'props.system.loggedIn') ? (
      <Router history={history}>
        <LoggedIn>
          <Route path="/oeci" component={OECIlogin} />
          <Route path="/recordsearch" component={RecordSearch} />
        </LoggedIn>
      </Router>
    ) : (
      <Router history={history}>
        <Route exact path="/" component={LogIn} />
        <Route exact path="/" component={Footer} />
        <Route path="/forgotpassword" component={ForgotPassword} />
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
