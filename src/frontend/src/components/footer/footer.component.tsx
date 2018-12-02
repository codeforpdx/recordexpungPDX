import * as React from 'react';

export class FooterComponent extends React.Component {

    public render() {
        return(
            <div className="footer bg-white shadow black-50">
                <a className="link underline hover-blue" href="#">Copyright</a>
                <a className="link underline hover-blue" href="#">Terms</a>
            </div>
        );
    }
}
