import React from 'react';
import LoggedInHeader from '../LoggedInHeader';

class LoggedIn extends React.Component {
  public render() {
    return (
      <div className="center">
        <LoggedInHeader />
        {this.props.children}
      </div>
    );
  }
}

export default LoggedIn;
