import React from 'react';
import { Redirect, Route, Router, Switch } from 'react-router-dom';
import history from '../../service/history';

import LogIn from '../LogIn';
import AllRecords from '../../containers/AllRecords';
import OeciLogin from '../OeciLogin';
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';
import Admin from '../Admin';

import AuthenticatedRoute from '../AuthenticatedRoute';
import PublicRoute from '../PublicRoute';
import InterimPage from '../InterimPage';

class AppRouter extends React.Component {
  public redirect = () => <Redirect to="/" />;

  public render() {
    return (
      <Router history={history}>
        <Switch>
          <AuthenticatedRoute path="/oeci" component={OeciLogin} />
          <AuthenticatedRoute path="/record-search" component={AllRecords} />
          <AuthenticatedRoute path="/stats" component={InterimPage} />
          <AuthenticatedRoute path="/admin" component={Admin} />
          <AuthenticatedRoute path="/account" component={InterimPage} />

          <PublicRoute exact={true} path="/" component={LogIn} />
          <PublicRoute path="/forgot-password" component={ForgotPassword} />
          <PublicRoute path="/password-reset" component={PasswordReset} />

          {/* This route catches undefined url entries and redirects back to app
              we could put a 404 page in place at some point */}
          <Route render={this.redirect} />
        </Switch>
      </Router>
    );
  }
}

export default AppRouter;
