import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";

export default class Header extends React.Component {
  public render() {
    return (
      <div className="bg-white shadow">
        <nav 
          className="mw8 relative center flex flex-wrap justify-between pa3"
          aria-label="Primary"
        >
          <div className="logo mb4 mb0-ns">
            <Link to="/" aria-label="Home">
              <Logo />
            </Link>
          </div>
          <div className="mt5 mt2-ns">
            <Link
              to="/manual"
              className="link hover-blue f5 fw6 pv2 ph0 ph3-ns mr4-ns"
            >
              Manual
            </Link>
            {/* 
            <Link
              to="/community"
              className="link hover-blue f5 fw6 pv2 ph0 ph3-ns mr4-ns"
            >
              Community
            </Link>
            */}
            <Link
              to="/record-search"
              className="absolute top-1 right-1 static-ns bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
            >
              Search
            </Link>
          </div>
        </nav>
      </div>
    );
  }
}
