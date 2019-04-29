import React from 'react';
import './styles.scss';
import { FooterComponent } from '../Footer';
import { LoginComponent } from '../Login';

class App extends React.Component {

    public render() {
        return (
            <main className="mw6 ph2 center">
                <LoginComponent/>
                <FooterComponent/>
            </main>
    );
  }
}

export default App;
