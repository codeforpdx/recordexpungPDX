import React from "react";
import Logo from "../Logo";

export default class Header extends React.Component {
  public render() {
    return (
      <div className="bg-white shadow">
        <nav className="mw8 relative center flex flex-wrap justify-between pa3">
          <div className="logo mb4 mb0-ns">
            <a href="/">
              <Logo />
            </a>
          </div>
          <div className="mt5 mt2-ns">
            <a
              href="/manual"
              className="link hover-blue f5 fw6 pv2 ph0 ph3-ns mr4-ns"
            >
              Manual
            </a>
            <a
              href="/record-search"
              className="absolute top-1 right-1 static-ns bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
            >
              Search
            </a>
          </div>
        </nav>
      </div>
    );
  }
}
