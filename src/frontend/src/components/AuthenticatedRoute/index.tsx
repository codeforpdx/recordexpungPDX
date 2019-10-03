import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { AppState } from '../../redux/store';
import { connect } from 'react-redux';
import { ReactComponentLike } from 'prop-types';

interface Props {
  component: ReactComponentLike;
  loggedIn: boolean;
  path: string;
}

class AuthenticatedRoute extends React.Component<Props> {
  public isAuthenticated = () => this.props.loggedIn;

  public displayComponent = () => {
    const { component: Component, ...props } = this.props;

    // checks if there is current authentication:
    // if authenticated it renders the desired component
    // otherwise it redirects to the LogIn component
    return this.isAuthenticated() ? (
      <Component {...props} />
    ) : (
      <Redirect to="/" />
    );
  };

  public render() {
    return <Route render={this.displayComponent} />;
  }
}

const mapStateToProps = (state: AppState) => ({
  loggedIn: state.system.loggedIn
});

export default connect(mapStateToProps)(AuthenticatedRoute);
