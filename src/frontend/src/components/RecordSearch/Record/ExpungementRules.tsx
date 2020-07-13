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
      <div className="relative ph3  pb4">
        <div className="ml3 pl1">
          <Disclosure open={this.state.open} onChange={() => toggleOpen()}>
            <DisclosureButton>
              <span className="">More info </span>
              {this.state.open ? (
                <span aria-hidden="true" className="fas fa-angle-up"></span>
              ) : (
                <span aria-hidden="true" className="fas fa-angle-down"></span>
              )}
            </DisclosureButton>
            <DisclosurePanel className="pt4">
              {rules.split("\n").map((line: string, index: number) => {
                return (
                  <div className="mb2" key={index}>
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
