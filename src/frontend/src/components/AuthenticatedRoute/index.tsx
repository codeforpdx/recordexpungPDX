import React, { ComponentClass } from 'react';
import { Route, Redirect } from 'react-router-dom';

interface Props {
  component: ComponentClass;
  isAuthenticated: boolean;
  path: string;
}

const AuthenticatedRoute = ({
  component: Component,
  isAuthenticated,
  ...rest
}: Props) => (
  <Route
    {...rest}
    render={props =>
      isAuthenticated ? <Component {...props} /> : <Redirect to="/" />
    }
  />
);

export default AuthenticatedRoute;
