import React from "react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { oeciLogout } from "../../service/cookie-service";
import store, { RootState } from "../../redux/store";
import { setLoggedIn } from "../../redux/authSlice";

import Logo from "../Logo";

type HeaderProps = {
  isLoggedIn: boolean;
};

const mapStateToProps = (state: RootState) => ({
  isLoggedIn: state.auth.loggedIn,
});

function Header({ isLoggedIn }: HeaderProps) {
  const handleLogOut = () => {
    oeciLogout();
    store.dispatch(setLoggedIn(false));
  };

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
          {isLoggedIn && (
            <button
              onClick={handleLogOut}
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

export default connect(mapStateToProps)(Header);
