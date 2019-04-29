import React from 'react';
import { connect } from "react-redux";
import { get } from 'lodash';
import './styles.scss';
import { AppState } from "../../redux/store";

import Footer from '../Footer';
import Login from '../Login';
import LoggedIn from '../LoggedIn';
import RecordSearch from '../RecordSearch';

class App extends React.Component {
  public render() {
    return (
      get(this, 'props.system.loggedIn') ?
        <LoggedIn>
          <RecordSearch/>
        </LoggedIn>
        :
        <main className="mw6 ph2 center">
          <Login/>
          <Footer/>
        </main>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system,
});

export default connect(mapStateToProps, {})(App);