import React from "react";

export default class Footer extends React.Component {
  public render() {
    return (
      <footer className="mw8 center bg-white pt5 pb6 ph4">
        <a className="dib link hover-blue bb mr5 mb4" href="/privacy-policy">
          Privacy Policy
        </a>
        <a className="dib link hover-blue bb mr5 mb4" href="/faq">
          FAQ
        </a>
        <a className="dib link hover-blue bb" href="/appendix">
          Appendix
        </a>
      </footer>
    );
  }
}
