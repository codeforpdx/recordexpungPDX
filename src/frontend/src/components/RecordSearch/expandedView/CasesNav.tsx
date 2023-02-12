import React from "react";
import { CaseData, ChargeData } from "../Record/types";
import { getEligibilityAttributes } from "../Record/util";
import Link from "../../common/Link";
import Aside from "../../common/Aside";

function Charge({
  chargeData,
  caseBalance,
}: {
  chargeData: ChargeData;
  caseBalance: number;
  isLast: boolean;
}) {
  const { ambiguous_charge_id: id, name, expungement_result } = chargeData;
  const { color, bgColor, icon } = getEligibilityAttributes(
    expungement_result,
    caseBalance
  );

  return (
    <li className="pv1 flex-ns flex-wrap" id={"scroll-spy-target-" + id}>
      <div className="w-1 pb1 pr1 pb0-ns">
        <span
          className={`${color} ${bgColor} pv1 ph2 mr1 dib br3 relative z-1`}
        >
          <span className={icon}></span>
        </span>
      </div>
      <div className="w-80 pb1 pb0-ns">
        <Link to={"#" + id} text={name} />
      </div>
    </li>
  );
}

function Case({ caseData, idx }: { caseData: CaseData; idx: number }) {
  const { date, case_number, charges, balance_due } = caseData;

  return (
    <div className="pb1">
      <div
        className="fw6 lh-copy flex flex-wrap pv1 ph2"
        id={"scroll-spy-target-" + case_number}
      >
        <div className="w-50">
          <span className="pr2">{idx + 1})</span>
          <Link to={"#" + case_number} text={"#" + case_number} />
        </div>
        <div className="w-50 pl3">{date}</div>
      </div>
      <ul className="list">
        {charges.length > 0 ? (
          charges.map((chargeData, idx2, arr) => (
            <Charge
              key={chargeData.ambiguous_charge_id + chargeData.case_number}
              chargeData={chargeData}
              caseBalance={balance_due}
              isLast={idx2 === arr.length - 1}
            />
          ))
        ) : (
          <Aside text="Excluded charge(s) are hidden." />
        )}
      </ul>
    </div>
  );
}

interface Props extends React.HTMLAttributes<HTMLElement> {
  cases: CaseData[];
}

export default function CasesNavList({ cases, ...props }: Props) {
  return (
    <div {...props}>
      {cases.map((caseData, idx) => {
        return (
          <Case key={caseData.case_number} caseData={caseData} idx={idx} />
        );
      })}
    </div>
  );
}
