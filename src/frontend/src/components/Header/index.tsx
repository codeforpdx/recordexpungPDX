import React from 'react';
import LogOut from '../LogOut';
import Logo from '../Logo';
import history from '../../service/history';
import { AppState } from '../../redux/store';
import { connect } from 'react-redux';

interface Props {
  isAuthenticated: boolean;
  isAdmin?: boolean;
}

class Header extends React.Component<Props> {
  public render() {
    return (
      this.props.isAuthenticated ? (
      <nav className="center pt3 ph2 bg-white shadow">
        <div className="mw8 center flex-l justify-between">
            <div className="logo mb3 mb0-l">
              <Logo />
            </div>

          <div className="dib mb3">

              <button
                onClick={() => history.push('/record-search')}
                className="link mid-gray hover-blue f6 f5-ns dib pa3"
              >
              Search
              </button>
            <button
              onClick={() => history.push('/manual')}
              className="link mid-gray hover-blue f6 f5-ns dib pa3"
            >
              Manual
            </button>

            {this.props.isAdmin ? (
              <button
                onClick={() => history.push('/admin')}
                className="link mid-gray hover-blue f6 f5-ns dib pa3"
              >
                Admin
              </button>
            ) : null}
            {this.props.isAdmin ? (
              <button
                onClick={() => history.push('/account')}
                className="link mid-gray hover-blue f6 f5-ns dib pa3"
              >
                Account
              </button>
            ) : null}

              <LogOut>
              {/* Nesting the button within a <Link> tag here would
                render but creates invalid HTML.
                https://stackoverflow.com/questions/42463263/wrapping-a-react-router-link-in-an-html-button
              */}
              <button
                onClick={() => history.push('/')}
                className="link mid-gray hover-blue f6 f5-ns dib pa3"
              >
                Log Out
              </button>

            </LogOut>
          </div>
        </div>
      </nav> ) : (
            <div className="bg-white">
              <nav className="mw8 relative center flex flex-wrap justify-between ph3 pb4 pt3 pt4-ns">
                <div className="logo--landing-page mb4 mb0-ns">
                  <a href="/"><Logo /></a>
                </div>
                <div className="mt5 mt0-ns">
                  <a href="/manual"
                    className="link hover-blue f5 fw6 pv2 ph0 ph3-ns mr4-ns"
                  >
                    Manual
                  </a>
                  <a href="/login"
                    className="absolute top-1 right-1 static-ns bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
                  >
                    Log In
                  </a>
                </div>

              </nav>
            </div> )
    )
  }
}

const mapStateToProps = (state: AppState) => ({
  isAuthenticated: state.system.loggedIn,
  isAdmin: state.system.isAdmin
});

export default connect(mapStateToProps)(Header);
