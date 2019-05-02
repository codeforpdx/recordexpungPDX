import React from 'react';
import './styles.scss';

export class Footer extends React.Component {
  public render() {
    return(
      <footer className="mw8 ph3 center pv6 black-50">
        <button className="pr3 link underline hover-blue">Copyright</button>
        <button className="pr3 link underline hover-blue">Terms</button>
      </footer>
    );
  }
}

export default Footer;
