import React from 'react';
import UserList from '../UserList/index';

class Admin extends React.Component {
  public render() {
    return (
      <main className="mw8 center ph2">
        <UserList />
      </main>
    );
  }
}

export default Admin;
