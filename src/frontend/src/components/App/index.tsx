import React from "react";
import { Redirect, Route, Router, Switch } from "react-router-dom";
import history from "../../service/history";

import Footer from "../Footer";
import Header from "../Header";
import RecordSearch from "../RecordSearch";
import Demo from "../RecordSearch/Demo";
import OeciLogin from "../OeciLogin";
import Landing from "../Landing";
import Manual from "../Manual";
import Faq from "../Faq";
import Appendix from "../Appendix";
import PrivacyPolicy from "../PrivacyPolicy";
import UserForm from "../FormFilling";

class App extends React.Component {
  redirect = () => <Redirect to="/" />;
  public render() {
    return (
      <Router history={history}>
        <Header />
        <Switch>
          <Route component={Landing} exact={true} path="/" />
          <Route component={OeciLogin} path="/oeci" />
          <Route component={RecordSearch} path="/record-search" />
          <Route component={Demo} path="/demo-record-search" />
          <Route component={Manual} path="/manual" />
          <Route component={Faq} path="/faq" />
          <Route component={Appendix} path="/appendix" />
          <Route component={PrivacyPolicy} path="/privacy-policy" />
          <Route component={UserForm} path="/fill-expungement-forms" />
          <Route render={this.redirect} />
        </Switch>
        <Footer />
      </Router>
    );
  }
}

export default App;
