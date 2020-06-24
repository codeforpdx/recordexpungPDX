import React from "react";
import { Redirect, Route, Router, Switch } from "react-router-dom";
import history from "../../service/history";

import RecordSearch from "../RecordSearch";
import OeciLogin from "../OeciLogin";
import Landing from "../Landing";
import Manual from "../Manual";
import Faq from "../Faq";
import Appendix from "../Appendix";
import PrivacyPolicy from "../PrivacyPolicy";

class AppRouter extends React.Component {
  public redirect = () => <Redirect to="/" />;

  public render() {
    return (
      <Router history={history}>
        <Switch>
          <Route component={Landing} exact={true} path="/" />
          <Route component={OeciLogin} path="/oeci" />
          <Route component={RecordSearch} path="/record-search" />
          <Route component={Manual} path="/manual" />
          <Route component={Faq} path="/faq" />
          <Route component={Appendix} path="/appendix" />
          <Route component={PrivacyPolicy} path="/privacy-policy" />

          {/* This route catches undefined url entries and redirects back to app
              we could put a 404 page in place at some point */}
          <Route render={this.redirect} />
        </Switch>
      </Router>
    );
  }
}

export default AppRouter;
