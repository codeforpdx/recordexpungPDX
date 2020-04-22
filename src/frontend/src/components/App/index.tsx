import React from 'react';
import AppRouter from '../AppRouter';
import Footer from '../Footer';
import Authenticator from '../Authenticator';

class App extends React.Component {
  public render() {
    return (
      <Authenticator>
        <AppRouter />
        <Footer />
      </Authenticator>
    );
  }
}

export default App;
