import React from 'react';
import { Redirect, Route, Router, Switch } from 'react-router-dom';
import history from '../../service/history';

import LogIn from '../LogIn';
import AddUser from '../AddUser';
import EditUser from '../EditUser';
import RecordSearch from '../RecordSearch';
import OeciLogin from '../OeciLogin';
import ForgotPassword from '../ForgotPassword';
import PasswordReset from '../PasswordReset';
import Admin from '../Admin';
import AuthenticatedRoute from '../AuthenticatedRoute';
import PublicRoute from '../PublicRoute';
import InterimPage from '../InterimPage';
import Landing from '../Landing';

class AppRouter extends React.Component {
  public redirect = () => <Redirect to="/" />;

  public render() {
    return (
      <Router history={history}>
        <Switch>
          <AuthenticatedRoute path="/oeci" component={OeciLogin} />
          <AuthenticatedRoute path="/record-search" component={RecordSearch} />
          <AuthenticatedRoute path="/stats" component={InterimPage} />
          <AuthenticatedRoute path="/admin" component={Admin} />
          <AuthenticatedRoute path="/account" component={InterimPage} />
          <AuthenticatedRoute path="/add-user" component={AddUser} />
          <AuthenticatedRoute path="/edit-user" component={EditUser} />

          <PublicRoute exact={true} path="/" component={Landing} />
          <PublicRoute path="/login" component={LogIn} />
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
