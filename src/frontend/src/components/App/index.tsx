import React from 'react';
import AppRouter from '../AppRouter';
import Footer from '../Footer';
import Authenticator from '../Authenticator';

class App extends React.Component {
  public render() {
    return (
      <Authenticator>
        {/*<Header /> // added to individual pages and excluded from others */}
        <AppRouter />
        <Footer />
      </Authenticator>
    );
  }
}

export default App;
