import * as React from 'react';
import { FooterComponent } from "../footer/footer.component";
import { LoginComponent } from "../login/login.component";
import './App.style.scss';

class App extends React.Component {

    public render() {
        return (
            <div className="view-port">
                <main className="mw6 ph2 center">
                    <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
                        <LoginComponent/>
                    </section>
                    <div className="footer--wrapper">
                        <FooterComponent/>
                    </div>
                </main>
            </div>
    );
  }
}

export default App;
