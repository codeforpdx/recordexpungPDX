import * as React from 'react';
import { LoginComponent } from "../login/login.component";
import './App.style.scss';

class App extends React.Component {

    public render() {
        return (
            <div className="landing-container bg-gray-blue">
                <LoginComponent/>
            </div>
    );
  }
}

export default App;
