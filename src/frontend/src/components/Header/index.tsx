import React from 'react';
import LogOut from '../LogOut';
import Logo from '../Logo';
import history from '../../service/history';
import { AppState } from '../../redux/store';
import { connect } from 'react-redux';

interface Props {
  isAuthenticated: boolean;
}

class Header extends React.Component<Props> {
  public render() {
    return this.props.isAuthenticated ? (
      <nav className="center pt4 ph2 bg-white shadow">
        <div className="mw8 center flex-l justify-between">
          <div className="mb4">
            <Logo />
          </div>
          <div className="dib mb4">
            <button
              onClick={() => history.push('/record-search')}
              className="link hover-blue f6 f5-ns dib pa3"
            >
              Search
            </button>
            <button
              onClick={() => history.push('/stats')}
              className="link hover-blue f6 f5-ns dib pa3"
            >
              Stats
            </button>
            <button
              onClick={() => history.push('/admin')}
              className="link hover-blue f6 f5-ns dib pa3"
            >
              Admin
            </button>
            <button
              onClick={() => history.push('/account')}
              className="link hover-blue f6 f5-ns dib pa3"
            >
              Account
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
    ) : null;
  }
}

const mapStateToProps = (state: AppState) => ({
  isAuthenticated: state.system.loggedIn
});

export default connect(mapStateToProps)(Header);
