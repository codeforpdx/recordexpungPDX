import React from "react";
import { ExpungementRulesData } from "./types";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";
interface Props {
  expungement_rules: ExpungementRulesData;
}

export default class ExpungementRules extends React.Component<
  Props,
  { open: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = {
      open: false,
    };
  }
  render() {
    const toggleOpen = () => {
      this.setState({ open: !this.state.open });
    };
    const rules = this.props.expungement_rules;
    return (
      <div className="relative mb3 connect connect-type">
        <div className="ml3 pl1">
          <Disclosure open={this.state.open} onChange={() => toggleOpen()}>
            <DisclosureButton>
              <span className="fw7">More info</span>
              {this.state.open ? (
                <span aria-hidden="true" className="fas fa-angle-up"></span>
              ) : (
                <span aria-hidden="true" className="fas fa-angle-down"></span>
              )}
            </DisclosureButton>
            <DisclosurePanel>{rules + " "}</DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    );
  }
}
