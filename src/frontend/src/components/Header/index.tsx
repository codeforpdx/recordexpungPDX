import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";

export default class Header extends React.Component {
  state = {
    isOpen: false,
  };

  toggleMenu = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  public render() {
    const { isOpen } = this.state;

    return (
      <header className="fixed top-0 w-100 z-max bg-white shadow-4">
        <nav 
          className="flex justify-between items-center pa3 center mw9 relative h3-l"
          aria-label="Primary"
        >
          {/* LOGO SECTION 
              - 'w4': Fixed width (~128px) applied globally (no -l override).
              - 'h-auto': Maintains aspect ratio.
          */}
          <div className="flex-shrink-0 z-max mr3">
            <Link to="/" aria-label="Home" className="link db flex items-center">
              <Logo className="db w4 h-auto blue" />
            </Link>
          </div>

          {/* HAMBURGER BUTTON */}
          <button 
            className="db dn-l pointer bg-transparent bn pa2 z-max"
            onClick={this.toggleMenu}
            aria-label="Toggle navigation"
          >
            <div className="w2">
              <div className={`bg-dark-gray mb1 br-pill ${isOpen ? "rotate-45 absolute" : ""}`} 
                   style={{ height: '3px', width: '25px', transition: '0.4s' }}></div>
              <div className={`bg-dark-gray mb1 br-pill ${isOpen ? "dn" : ""}`} 
                   style={{ height: '3px', width: '25px', transition: '0.4s' }}></div>
              <div className={`bg-dark-gray br-pill ${isOpen ? "rotate-135 absolute" : ""}`} 
                   style={{ height: '3px', width: '25px', transition: '0.4s' }}></div>
            </div>
          </button>

          {/* NAVIGATION LINKS 
              - 'left-0 top-100 w-100': Replicates the full-width mobile dropdown placement.
              - 'pl5': Replicates the 50px mobile padding.
              - 'static-l w-auto-l': Resets to a horizontal row on desktop.
          */}
          <div className={`
            ${isOpen ? "flex flex-column absolute left-0 top-100 w-100 bg-white pa4 shadow-5 z-999" : "dn"} 
            flex-l items-center-l static-l pa0-l shadow-none-l w-auto-l
          `}>
            <Link 
              className="link navy hover-blue f5 fw6 pv2 ph3-l mr4-l pl5 pl3-l" 
              to="/about" 
              onClick={() => isOpen && this.toggleMenu()}
            >
              About Us
            </Link>
            <Link 
              className="link navy hover-blue f5 fw6 pv2 ph3-l mr4-l pl5 pl3-l" 
              to="/partner-interest" 
              onClick={() => isOpen && this.toggleMenu()}
            >
              Hey Partner
            </Link>
            <Link 
              className="link navy hover-blue f5 fw6 pv2 ph3-l mr4-l pl5 pl3-l" 
              to="/faq" 
              onClick={() => isOpen && this.toggleMenu()}
            >
              Common Myths
            </Link>
            <Link 
              className="link navy hover-blue f5 fw6 pv2 ph3-l mr4-l pl5 pl3-l" 
              to="/community" 
              onClick={() => isOpen && this.toggleMenu()}
            >
              Community Board
            </Link>
            <Link 
              className="link navy hover-blue f5 fw6 pv2 ph3-l mr4-l pl5 pl3-l" 
              to="/manual" 
              onClick={() => isOpen && this.toggleMenu()}
            >
              Manual
            </Link>
            
            <Link
              to="/record-search"
              className="link f5 fw6 pv2 ph3 blue br2 ba b--blue hover-bg-dark-blue hover-white tc mt3 mt0-l ml5 ml0-l"
              onClick={() => isOpen && this.toggleMenu()}
            >
              Search
            </Link>
          </div>
        </nav>
      </header>
    );
  }
}