import React from 'react';
import UserList from '../UserList/index';
import GroupList from '../GroupList/index';

class Admin extends React.Component {
  public render() {
    return (
      <main className="mw8 center ph2">
        <GroupList />
        <UserList />
      </main>
    );
  }
}

export default Admin;
