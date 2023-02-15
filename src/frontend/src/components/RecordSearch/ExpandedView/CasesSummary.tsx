import React from "react";
import { CaseData, ChargeData } from "../Record/types";
import toDollars from "../../../service/currency-format";
import { getEligibilityAttributes } from "../Record/util";
import Link from "../../common/Link";
import Aside from "../../common/Aside";

interface Props {
  showColor: boolean;
  cases?: CaseData[];
}

function Charge({
  chargeData,
  caseBalance,
  showColor,
}: {
  chargeData: ChargeData;
  caseBalance: number;
} & Props) {
  const { name, expungement_result, disposition } = chargeData;
  const { label, color, bgColor, icon } = getEligibilityAttributes(
    expungement_result,
    caseBalance,
    false
  );
  return (
    <li className={`flex-ns flex-wrap`}>
      <div className="w-25-ns">
        <div
          className={`w-80 tc pa1 br3 bb b--white ${showColor ? color : ""} ${
            showColor ? bgColor : ""
          }`}
        >
          <div className={`flex flex-wrap`}>
            <span className={icon + " w-10"}></span>
            <span className="fw6 w-90 pl1">{label}</span>
          </div>
        </div>
      </div>
      <div className="w-20-ns pt1 pl2">
        {disposition.ruling.toLocaleUpperCase()}
      </div>
      <div className="w-50-ns pt1 pl2">{name}</div>
    </li>
  );
}

function Case({ caseData, showColor }: { caseData: CaseData } & Props) {
  const { date, case_number, charges, balance_due, location } = caseData;

  return (
    <div className={`mb1`}>
      <div
        className={`fw7 flex flex-wrap br3 mb1 pv1 pl2 ${
          showColor ? "bg-gray-blue-2" : ""
        }`}
      >
        <div className="w-25-ns w-50 pl4">{date}</div>
        <div className="w-20-ns w-50">
          <Link to={"#" + case_number} text={"#" + case_number} />
        </div>
        <div className="w-20-ns w-50">{location}</div>
        <div className="w-30-ns w-50">
          {balance_due > 0 && toDollars(balance_due)}
        </div>
      </div>
      <ul className="list">
        {charges.length > 0 ? (
          charges.map((chargeData, idx2, arr) => (
            <Charge
              key={chargeData.ambiguous_charge_id + chargeData.case_number}
              chargeData={chargeData}
              caseBalance={balance_due}
              showColor={showColor}
            />
          ))
        ) : (
          <Aside
            className="pl3 mt2"
            text="Excluded charge(s) are hidden for this case."
          />
        )}
      </ul>
    </div>
  );
}

export default function CasesSummary({ showColor, cases, ...props }: Props) {
  const casesLength = cases?.length ?? 0;

  if (!cases || casesLength === 0) return <></>;

  return (
    <div {...props}>
      {cases.map((caseData: CaseData, idx: number) => {
        return (
          <Case
            key={caseData.case_number}
            caseData={caseData}
            showColor={showColor}
          />
        );
      })}
    </div>
  );
}
