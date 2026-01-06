import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";
import { forEach } from "lodash";

export default class Header extends React.Component {
  // 1. Initialize state to track if menu is open
  state = {
    isOpen: false,
  };

  toggleMenu = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  public render() {
    const { isOpen } = this.state;

    return (
      <div 
        className="header-wrapper bg-white shadow"
        style={{ position: "sticky", zIndex: "1000000", top: "0px", backgroundColor: "rgba(255,255,255)" }}
      >
        <nav 
          id="nav-nav"
          className="relative flex flex-wrap justify-between items-center pa3 center"
          style={{ maxWidth: "90vw" }}
          aria-label="Primary"
        >
          <div className="logo">
            <Link to="/" aria-label="Home">
              <Logo />
            </Link>
          </div>

          {/* 2. Hamburger Button - Only visible via CSS on small screens */}
          <button 
            className="hamburger-btn pointer bg-transparent bn"
            onClick={this.toggleMenu}
            aria-label="Toggle navigation"
          >
            <div className={`bar ${isOpen ? "open" : ""}`}></div>
            <div className={`bar ${isOpen ? "open" : ""}`}></div>
            <div className={`bar ${isOpen ? "open" : ""}`}></div>
          </button>

          {/* 3. Navigation Items - Class toggled based on state */}
          <div id="nav-items" className={`nav-links ${isOpen ? "is-open" : ""}`}>
            <Link className="link hover-blue f5 fw6 pv2 ph3-ns mr4-ns" to="/about" onClick={this.toggleMenu}>
              About Us
            </Link>
            <Link className="link hover-blue f5 fw6 pv2 ph3-ns mr4-ns" to="/partner-interest" onClick={this.toggleMenu}>
              Hey Partner
            </Link>
            <Link className="link hover-blue f5 fw6 pv2 ph3-ns mr4-ns" to="/faq" onClick={this.toggleMenu}>
              Common Myths
            </Link>
            <Link className="link hover-blue f5 fw6 pv2 ph3-ns mr4-ns" to="/community" onClick={this.toggleMenu}>
              Community Page
            </Link>
            <Link className="link hover-blue f5 fw6 pv2 ph3-ns mr4-ns" to="/manual" onClick={this.toggleMenu}>
              Manual
            </Link>
            <Link
              to="/record-search"
              className="search-link f5 fw6 pv2 ph3 blue br2 hover-bg-dark-blue hover-white"
              onClick={this.toggleMenu}
            >
              Search
            </Link>
          </div>
        </nav>

        <style>{`
          /* Desktop Default */
          .hamburger-btn { display: none; }
          .nav-links { display: flex; align-items: center; }

          /* Mobile Logic (< 1000px) */
          @media (max-width: 1000px) {
            .hamburger-btn {
              display: block;
              z-index: 1001;
            }

            /* Hamburger Lines */
            .bar {
              width: 25px;
              height: 3px;
              background-color: #333;
              margin: 5px 0;
              transition: 0.4s;
            }

            /* Animate to "X" when open */
            .bar.open:nth-child(1) { transform: rotate(-45deg) translate(-5px, 6px); }
            .bar.open:nth-child(2) { opacity: 0; }
            .bar.open:nth-child(3) { transform: rotate(45deg) translate(-5px, -6px); }

            /* Dropdown Menu Styling */
            .nav-links {
              display: none; /* Hidden by default */
              flex-direction: column;
              // width: 100%;
              background: white;
              position: absolute;
              top: 100%;
              left: -43px;
              padding: 20px;
              box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }

            .nav-links.is-open {
              display: flex; /* Show when clicked */
            }

            .nav-links a {
              margin-bottom: 15px;
              width: 100%;
              text-align: left;
              padding-left: 50px;
            }

            .search-link {
              position: static !important; /* Remove the absolute positioning from your original code on mobile */
              margin-top: 10px;
              margin-right: 1.75rem;
            }
          }
        `}</style>
      </div>
    );
  }
}
