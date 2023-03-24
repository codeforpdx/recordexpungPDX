import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import Logo from "../Logo";
import { isLoggedIn, oeciLogout } from "../../service/cookie-service";

export default function Header() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const location = useLocation();

  useEffect(() => {
    setLoggedIn(isLoggedIn());
  }, [location]);

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
          <Link
            to="/record-search"
            className="absolute top-1 right-1 static-ns bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
          >
            Search
          </Link>
          {loggedIn && (
            <button
              onClick={oeciLogout}
              className="absolute top-1 left-2 static-ns bg-white f5 fw6 br2 ba b--blue blue link hover-dark-blue pv2 ph3 ml2"
            >
              Log Out
            </button>
          )}
        </div>
      </nav>
    </div>
  );
}
