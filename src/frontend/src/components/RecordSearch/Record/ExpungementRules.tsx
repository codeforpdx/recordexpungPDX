import React from "react";
import useDisclosure from "../../../hooks/useDisclosure";
import { buildRule } from "../../Rules/ChargeTypeRule";
import DisclosureIcon from "../../common/DisclosureIcon";

interface Props {
  expungement_rules: string;
}

export default function ExpungementRules({ expungement_rules }: Props) {
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useDisclosure();

  return (
    <div className="bt b--light-gray pt2 mh3 pb2">
      <button {...disclosureButtonProps}>
        <span className="flex items-center fw5 mid-gray link hover-blue pb1">
          More Info
          <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
        </span>
      </button>
      <div {...disclosureContentProps} className="pt2">
        {buildRule(expungement_rules)}
      </div>
    </div>
  );
}
