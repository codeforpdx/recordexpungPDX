import * as React from 'react';

export class FooterComponent extends React.Component {

    public render() {
        return(
            <footer className="mw8 ph3 center pv6 black-50">
              <a className="pr3 link underline hover-blue" href="#">Copyright</a>
              <a className="pr3 link underline hover-blue" href="#">Terms</a>
            </footer>
        );
    }
}
