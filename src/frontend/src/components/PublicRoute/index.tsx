import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { AppState } from '../../redux/store';
import { connect } from 'react-redux';
import { ReactComponentLike } from 'prop-types';

interface Props {
  component: ReactComponentLike;
  loggedIn: boolean;
  path: string;
  exact?: boolean;
}

class PublicRoute extends React.Component<Props> {
  public isAuthenticated = () => this.props.loggedIn;

  public displayComponent = () => {
    const { component: Component, ...props } = this.props;

    // checks if there is current authentication:
    // if authenticated it redirects to the OECI login
    // otherwise it renders the desired component
    return this.isAuthenticated() ? (
      <Redirect to="/oeci" />
    ) : (
      <Component {...props} />
    );
  };

  public render() {
    return <Route render={this.displayComponent} />;
  }
}

const mapStateToProps = (state: AppState) => ({
  loggedIn: state.system.loggedIn
});

export default connect(mapStateToProps)(PublicRoute);
