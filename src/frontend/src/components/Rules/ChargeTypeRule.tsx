import React from "react";
import useDisclosure from "../../hooks/useDisclosure";
import DisclosureIcon from "../common/DisclosureIcon";

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

export default function ChargeTypeRule({ open, rule }: Props) {
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useDisclosure({ isOpenToStart: open });

  return (
    <div className="mb2" id={rule.charge_type_class_name}>
      <button {...disclosureButtonProps}>
        <span className="flex items-center tracked-tight fw5 mid-gray link hover-blue pb1">
          {rule.charge_type_name}
          <DisclosureIcon
            disclosureIsExpanded={disclosureIsExpanded}
            className="pt1 pl1"
          />
        </span>
      </button>
      <div {...disclosureContentProps} className="ma2 lh-copy">
        {buildRule(rule.expungement_rules)}
      </div>
    </div>
  );
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
        {rules[1].map((element: any, index: number) => {
          return (
            <li key={index} className="ml2">
              {element}
            </li>
          );
        })}
      </ul>
    );
  } else {
    return rules.map((element: any) => {
      return buildRule(element);
    });
  }
}
