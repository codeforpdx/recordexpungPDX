import React from 'react';
import { Switch, Route } from 'react-router-dom';
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
        <Switch>
          <Route path="/search" component={RecordSearch} />
          <Route path="/stats" /*component={}*/ />
          <Route path="/admin" /*component={}*/ />
          <Route path="/account" /*component={}*/ />
          <Route component={RecordSearch} />
        </Switch>
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
