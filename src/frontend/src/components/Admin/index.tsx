import React from 'react';
import UserList from '../UserList/index';
import Header from '../Header';

class Admin extends React.Component {
  public render() {
    // The GroupList component should be left off of this page until the feature is fully implemented
    return (
      <>
      <Header/>
      <main className="mw8 center ph2">
        <UserList />
      </main>
      </>
    );
  }
}

export default Admin;
