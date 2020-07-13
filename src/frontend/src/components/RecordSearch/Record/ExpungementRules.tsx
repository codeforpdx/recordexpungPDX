import React from "react";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";

interface Props {
  expungement_rules: string;
}

interface State {
  open: boolean;
}

export default class ExpungementRules extends React.Component<Props, State> {
  state = {
    open: false,
  };

  render() {
    const toggleOpen = () => {
      this.setState({ open: !this.state.open });
    };
    const rules = this.props.expungement_rules;
    return (
      <div className="bt b--light-gray pt2 mh3 pb2">
        <div className="">
          <Disclosure open={this.state.open} onChange={() => toggleOpen()}>
            <DisclosureButton>
              <span className="flex items-center tracked-tight fw5 mid-gray link hover-blue pb1">
                More Info
                {this.state.open ? (
                  <span aria-hidden="true" className="fas fa-angle-up pt1 pl1"></span>
                ) : (
                  <span aria-hidden="true" className="fas fa-angle-down pt1 pl1"></span>
                )}
              </span>
            </DisclosureButton>
            <DisclosurePanel className="pt2">
              {rules.split("\n").map((line: string, index: number) => {
                return (
                  <div className="lh-copy mb2" key={index}>
                    {line}
                  </div>
                );
              })}
            </DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    );
  }
}
