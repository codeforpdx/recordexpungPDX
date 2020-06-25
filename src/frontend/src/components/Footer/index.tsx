import React from "react";

export default class Footer extends React.Component {
  public render() {
    return (
      <footer className="mw8 center bg-white pt5 pb6 ph4">
        <a className="link hover-blue underline pr5" href="/privacy-policy">
          Privacy Policy
        </a>
        <a className="link hover-blue underline pr5 pl4" href="/faq">
          FAQ
        </a>
        <a className="link hover-blue underline pl4" href="/appendix">
          Appendix
        </a>
      </footer>
    );
  }
}
