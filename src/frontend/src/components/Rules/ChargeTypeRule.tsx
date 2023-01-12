import React from "react";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";

export interface TypeRuleData {
  charge_type_name: string;
  charge_type_class_name: string;
  expungement_rules: string;
}

export interface RulesData {
  charge_types: TypeRuleData[];
}

interface Props {
  rule: TypeRuleData;
  open: boolean;
}

interface State {
  open: boolean;
}

export default class ChargeTypeRule extends React.Component<Props, State> {
  state = {
    open: this.props.open,
  };
  toggleOpen = () => {
    this.setState({ open: !this.state.open });
  };

  componentWillReceiveProps(newProps: Props) {
    this.setState({ open: newProps.open });
  }

  render() {
    return (
      <div className="mb2" id={this.props.rule.charge_type_class_name}>
        <Disclosure open={this.state.open} onChange={() => this.toggleOpen()}>
          <DisclosureButton>
            <span className="flex items-center tracked-tight fw5 mid-gray link hover-blue pb1">
              {this.props.rule.charge_type_name}
              {this.state.open ? (
                <span
                  aria-hidden="true"
                  className="fas fa-angle-up pt1 pl1"
                ></span>
              ) : (
                <span
                  aria-hidden="true"
                  className="fas fa-angle-down pt1 pl1"
                ></span>
              )}
            </span>
          </DisclosureButton>
          <DisclosurePanel>
            <div className="ma2 lh-copy">
              {buildRule(this.props.rule.expungement_rules)}
            </div>
          </DisclosurePanel>
        </Disclosure>
      </div>
    );
  }
}

export function buildRule(rules: any) {
  if (typeof rules === "string") {
    return rules.split("\n").map((line: string, index: number) => {
      return (
        <div className="mb2" key={index}>
          {line}
        </div>
      );
    });
  } else if (rules[0] === "ul") {
    return (
      <ul className="ml3 mb2">
        {rules[1].map((element: any) => {
          return <li className="ml2">{element}</li>;
        })}
      </ul>
    );
  } else {
    return rules.map((element: any) => {
      return buildRule(element);
    });
  }
}
