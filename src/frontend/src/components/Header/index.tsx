import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";
import { hasOeciToken } from "../../service/cookie-service";
import { oeciLogOut } from "../../service/oeci";


interface State {
  isLoggedIn: boolean;
}

export default class Header extends React.Component {
  state: State = {
    isLoggedIn: false
  };

  componentDidMount(): void {
    this.setState({isLoggedIn: hasOeciToken()})
  }

  handleLogoutClick = () => {
    oeciLogOut()
    this.setState({isLoggedIn: false})
  }

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
            <Link
              to="/record-search"
              className="absolute top-1 right-1 static-ns bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
            >
              Search
            </Link>
            { this.state.isLoggedIn &&
              <button
                type="button"
                onClick={this.handleLogoutClick}
                className="link hover-blue f5 fw6 pv2 ph0 ph3-ns ml4-ns bg-white mid-gray br2 ba b--black-10"
              >
                Log Out
              </button>
            }
          </div>
        </nav>
      </div>
    );
  }
}
