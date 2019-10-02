import React from 'react';
import { Router, Switch } from 'react-router-dom';
import history from '../../service/history';

import LogIn from '../LogIn';
import RecordSearch from '../RecordSearch';
import OeciLogin from '../OeciLogin';
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';
import Admin from '../Admin';

import AuthenticatedRoute from '../AuthenticatedRoute';
import PublicRoute from '../PublicRoute';
import InterimPage from '../InterimPage';

class AppRouter extends React.Component {
  public render() {
    return (
      <Router history={history}>
        <Switch>
          <AuthenticatedRoute path="/oeci" component={OeciLogin} />
          <AuthenticatedRoute path="/record-search" component={RecordSearch} />
          <AuthenticatedRoute path="/stats" component={InterimPage} />
          <AuthenticatedRoute path="/admin" component={Admin} />
          <AuthenticatedRoute path="/account" component={InterimPage} />

          <PublicRoute exact={true} path="/" component={LogIn} />
          <PublicRoute path="/forgot-password" component={ForgotPassword} />
          <PublicRoute path="/password-reset" component={PasswordReset} />
        </Switch>
      </Router>
    );
  }
}

export default AppRouter;
