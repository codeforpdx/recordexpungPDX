import React from 'react';
import Logo from '../Logo';
import history from '../../service/history';
import {Link} from "react-router-dom";

export default class Header extends React.Component {
  public render() {
    return (
      <nav className="center pt3 ph2 bg-white shadow">
        <div className="mw8 center flex-l justify-between">
            <Link to="/">
              <div className="logo mb3 mb0-l">
                <Logo />
              </div>
            </Link>

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
          </div>
        </div>
      </nav>
    )
  }
}
