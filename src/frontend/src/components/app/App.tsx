import * as React from 'react';
import { FooterComponent } from "../footer/footer.component";
import { LoginComponent } from "../login/login.component";
import './App.style.scss';

class App extends React.Component {

    public render() {
        return (
            <div className="view-port">
                <div className="landing-container bg-gray-blue">
                    <LoginComponent/>
                </div>
                <div className="footer-wrapper bg-washed-green">
                    <FooterComponent/>
                </div>
            </div>
    );
  }
}

export default App;
