import React from "react";
import { Link } from "react-router-dom";

export default class Footer extends React.Component {
  public render() {
    return (
      <footer className="footer-main mw8 center f6 f5-l bg-white pt5 pb6 ph4">
        <div className="flex">
          <ul className="list mr5 mr6-ns">
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/"
                onClick={() => window.scrollTo(0, 0)}
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/partner-interest"
                onClick={() => window.scrollTo(0, 0)}
              >
                Hey Partner
              </Link>
            </li>
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/manual"
                onClick={() => window.scrollTo(0, 0)}
              >
                Manual
              </Link>
            </li>
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/record-search"
                onClick={() => window.scrollTo(0, 0)}
              >
                Search
              </Link>
            </li>
          </ul>
          <ul className="list">
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/faq"
                onClick={() => window.scrollTo(0, 0)}
              >
                FAQ
              </Link>
            </li>
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/appendix"
                onClick={() => window.scrollTo(0, 0)}
              >
                Appendix
              </Link>
            </li>
            <li>
              <Link
                className="dib link hover-blue bb mb3"
                to="/privacy-policy"
                onClick={() => window.scrollTo(0, 0)}
              >
                Privacy Policy
              </Link>
            </li>
          </ul>
        </div>
      </footer>
    );
  }
}
