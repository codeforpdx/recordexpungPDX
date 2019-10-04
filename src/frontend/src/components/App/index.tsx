import React from 'react';
import AppRouter from '../AppRouter';
import Header from '../Header';
import Footer from '../Footer';
import Authenticator from '../Authenticator';

class App extends React.Component {
  public render() {
    return (
      <Authenticator>
        <Header />
        <AppRouter />
        <Footer />
      </Authenticator>
    );
  }
}

export default App;
