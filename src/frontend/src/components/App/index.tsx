import React from 'react';
import { connect } from 'react-redux';
import { get } from 'lodash';
import { AppState } from '../../redux/store';

import Footer from '../Footer';
import LogIn from '../LogIn';
import LoggedIn from '../LoggedIn';
import RecordSearch from '../RecordSearch';

class App extends React.Component {
  public render() {
    return get(this, 'props.system.loggedIn') ? (
      <LoggedIn>
        <RecordSearch />
      </LoggedIn>
    ) : (
      <div>
        <LogIn />
        <Footer />
      </div>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  {}
)(App);
