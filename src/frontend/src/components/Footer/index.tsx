import React from "react";
import { Link } from "react-router-dom";

export default class Footer extends React.Component {
  public render() {
    return (
      <footer className="mw8 center bg-white pt5 pb6 ph4">
        <Link
          className="dib link hover-blue bb mr5 mb4"
          to="/privacy-policy"
          onClick={() => window.scrollTo(0, 0)}
        >
          Privacy Policy
        </Link>
        <Link
          className="dib link hover-blue bb mr5 mb4"
          to="/faq"
          onClick={() => window.scrollTo(0, 0)}
        >
          FAQ
        </Link>
        <Link
          className="dib link hover-blue bb"
          to="/appendix"
          onClick={() => window.scrollTo(0, 0)}
        >
          Appendix
        </Link>
      </footer>
    );
  }
}
