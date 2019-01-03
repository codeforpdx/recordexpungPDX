import * as React from 'react';
import { FooterComponent } from "../footer/footer.component";
import { LoginComponent } from "../login/login.component";

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
