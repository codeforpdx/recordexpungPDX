import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";

interface HeaderState {
  isOpen: boolean;
}

export default class Header extends React.Component<{}, HeaderState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      isOpen: false,
    };
  }

  private toggleMenu = (): void => {
    this.setState((prevState) => ({ isOpen: !prevState.isOpen }));
  };

  public render() {
    const { isOpen } = this.state;

    return (
      <header className="fixed top-0 w-100 z-max bg-white shadow-4">
        <nav
          className="relative flex flex-column flex-row-l justify-between-l items-center pa3 center mw9"
          aria-label="Primary"
        >
          <div className="w-100 w-auto-l flex justify-between items-center">
            <div className="logo">
              <Link to="/" aria-label="Home" className="mh4">
                <Logo className="" />
              </Link>
            </div>

            <button
              className="db dn-l pointer bg-transparent bn pa2 z-max"
              onClick={this.toggleMenu}
              aria-label="Toggle navigation"
            >
              <div className="w2 h1 relative pointer">
                <div
                  className={`bg-navy h-25 w-100 mb1 transition-all ${
                    isOpen ? "rotate-45 absolute top-0" : ""
                  }`}
                />
                <div
                  className={`bg-navy h-25 w-100 mb1 transition-all ${
                    isOpen ? "dn" : ""
                  }`}
                />
                <div
                  className={`bg-navy h-25 w-100 transition-all ${
                    isOpen ? "rotate-135 absolute top-0" : ""
                  }`}
                />
              </div>
            </button>
          </div>

          <div
            className={`${
              isOpen ? "flex" : "dn"
            } flex-l flex-column flex-row-l items-center static-l pa0-l shadow-none-l w-auto-l z-999 mt3 mt0-l`}
          >
            <Link
              className="link navy hover-blue f5 fw6 pv3 pv2-l ph3-l mr4-l nowrap"
              to="/community"
              onClick={this.toggleMenu}
            >
              Community Board
            </Link>
            <Link
              className="link navy hover-blue f5 fw6 pv3 pv2-l ph3-l mr4-l nowrap"
              to="/manual"
              onClick={this.toggleMenu}
            >
              Manual
            </Link>

            <Link
              to="/record-search"
              className="link f5 fw6 pv2 ph3 blue br2 ba b--blue hover-bg-dark-blue hover-white tc mt3 mt0-l ml4-l"
              onClick={this.toggleMenu}
            >
              Search
            </Link>
          </div>
        </nav>
      </header>
    );
  }
}
