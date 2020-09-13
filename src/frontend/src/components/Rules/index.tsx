import React from "react";
import axios, {
  AxiosPromise,
  AxiosRequestConfig,
  AxiosResponse,
  AxiosError,
} from "axios";
import { HashLink as Link } from "react-router-hash-link";

import ChargeTypeRule from "./ChargeTypeRule";
import { TypeRuleData, RulesData } from "./ChargeTypeRule";

interface Props {}

interface State {
  rules: RulesData;
  loaded: boolean;
  expandAll: boolean;
}

export default class Rules extends React.Component<Props, State> {

  state = {
    rules: { charge_types: [] },
    loaded: false,
    expandAll: false,
  };

  fetchRules = () => {
    axios
      .request({
        url: "/api/rules",
        method: "get",
      })
      .then((response: AxiosResponse) => {
        this.setState({ rules: response.data, loaded: true });
      })
      .catch((error: AxiosError) => {
        alert(error.message);
      });
  };

  componentDidMount() {
    document.title = "Rules - RecordSponge";
    if (!this.state.rules.charge_types[0]) {
      this.fetchRules();
    }
  }

  render() {
    return (
      this.state.loaded && (
        <>
          <main className="flex-l mw8 center ph4 mt5">
            <article className="order-1 lh-copy">
              <section className="mb5" id="rules">
                <h1 className="f2 fw9 mb3 mt4">Type Eligibility Rules</h1>
                <p className="mb2">
                  RecordSponge classifies every charge into one of{" "}
                  {this.state.rules.charge_types.length} different charge types.
                  These charge types are defined specifically for our analysis
                  and they are based on a collection of the charge's identifying
                  information in OECI such as severity level, statute, and class
                  name, and the particular subsections of expungement law that
                  determine their eligibility.
                </p>
                <p className="mb2">
                  This is a useful reference while using the{" "}
                  <Link className="bb hover-blue" to="/manual#editing">
                    Edit Results
                  </Link>{" "}
                  feature to select a charge type.
                </p>
                <p className="mb2">
                  The same information is provided in-line in record search
                  results for each charge, so this page is not essential reading
                  for typical use of RecordSponge. However, this is provided for
                  those interested in a complete view of our software logic.
                </p>
              </section>
              <section className="ml3 mb5" id="chargetypes">
                <h2 className="f3 fw9 mb1 mt4">Charge Types</h2>
                <button
                  className="link hover-blue gray mb3 ml2"
                  onClick={() => {
                    this.setState({ expandAll: !this.state.expandAll });
                  }}
                >
                  {" "}
                  {this.state.expandAll ? "Collapse All" : "Expand All"}{" "}
                </button>
                <div className="ml3">
                  {this.state.rules &&
                    this.state.rules.charge_types.map(
                      (item: TypeRuleData, index: number) => {
                        return (
                          <ChargeTypeRule
                            key={index}
                            rule={item}
                            open={this.state.expandAll}
                          />
                        );
                      }
                    )}
                </div>
              </section>
            </article>
          </main>
        </>
      )
    );
  }
}
