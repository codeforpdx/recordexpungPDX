import React from 'react';
import LogOut from '../LogOut';
import Logo from '../Logo';
import { Link } from 'react-router-dom';
import history from '../History';

class LoggedInHeader extends React.Component {
  public render() {
    return (
      <nav className="center pt4 ph2 bg-white shadow">
        <div className="mw8 center flex-l justify-between">
          <div className="mb4">
            <Logo />
          </div>
          <div className="dib mb4">
            <button className="link hover-blue f6 f5-ns dib pa3">
              <Link to="/record-search">Search</Link>
            </button>
            <button className="link hover-blue f6 f5-ns dib pa3">
              <Link to="/stats">Stats</Link>
            </button>
            <button className="link hover-blue f6 f5-ns dib pa3">
              <Link to="/admin">Admin</Link>
            </button>
            <button className="link hover-blue f6 f5-ns dib pa3">
              <Link to="/account">Account</Link>
            </button>
            <LogOut>
              {/* Nesting the button within a <Link> tag here would
                render but creates invalid HTML.
                https://stackoverflow.com/questions/42463263/wrapping-a-react-router-link-in-an-html-button
              */}
              <button
                onClick={() => history.push('/')}
                className="link hover-blue f6 f5-ns dib pa3"
              >
                Log Out
              </button>
            </LogOut>
          </div>
        </div>
      </nav>
    );
  }
}

export default LoggedInHeader;
