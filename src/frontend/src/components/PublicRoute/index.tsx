import React, { ComponentClass } from 'react';
import { Route, Redirect } from 'react-router-dom';
import history from '../../service/history';

interface Props {
  component: ComponentClass;
  isAuthenticated: boolean;
  path: string;
  exact?: boolean;
}

const PublicRoute = ({
  component: Component,
  isAuthenticated,
  ...rest
}: Props) => {
  const displayComponent = (props: any) => {
    console.log(props.location);
    if (!isAuthenticated) {
      return <Component />;
    } else {
      props.location.state ? history.goBack() : history.replace('/oeci');
    }
  };

  return (
    <Route {...rest} path="path" render={props => displayComponent(props)} />
    //   {displayComponent()}
    // </Route>
  );
};

export default PublicRoute;
