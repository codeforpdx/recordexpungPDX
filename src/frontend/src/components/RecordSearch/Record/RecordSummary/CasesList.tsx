import React from "react";
import { getEligibilityColor, getFinalEligibility } from "./utils";
import toDollars from "../../../../service/currency-format";
import { CaseData, ChargeData } from "../types";

function Charge({
  chargeData,
  caseBalance,
}: {
  chargeData: ChargeData;
  caseBalance: number;
}) {
  const { name, expungement_result, disposition } = chargeData;
  const { time_eligibility, type_eligibility } = expungement_result;

  let status = type_eligibility ? type_eligibility.status : "Unknown";
  let finalStatus = status;
  let dateEligible = "";

  if (time_eligibility) {
    dateEligible = time_eligibility.date_will_be_eligible;
    finalStatus = getFinalEligibility(status, dateEligible, caseBalance);
  }

  const color = getEligibilityColor(finalStatus);

  return (
    <li className="f6 pv1 flex-ns flex-wrap">
      <div className="w-30 pr4">
        <span
          className={`fw6 ${color} bg-washed-${
            color === "dark-blue" ? "blue" : color
          } pv1 ph2 dib br3 relative outline-2-white z-1`}
        >
          {finalStatus}
        </span>
      </div>
      <div className="w-70">
        <span className="lh-copy">{name}</span>{" "}
        <span className="lh-copy">
          ({disposition.ruling.toLocaleUpperCase()})
        </span>{" "}
      </div>
    </li>
  );
}

function Case({ caseData }: { caseData: CaseData }) {
  const { date, case_number, charges, balance_due } = caseData;

  return (
    <div className="mb3 pb1 bb b--light-gray">
      <div className="fw6 lh-copy">
        <div className="flex-ns flex-wrap">
          <div className="w-30">{date}</div>
          <div className="w-70">
            #
            <a href={"#" + case_number} className="link bb hover-blue">
              {case_number}
            </a>
          </div>
        </div>
      </div>
      <ul className="list">
        {charges.map((chargeData, idx2) => (
          <Charge
            key={idx2}
            chargeData={chargeData}
            caseBalance={balance_due}
          />
        ))}
      </ul>
      {balance_due > 0 && (
        <div className="flex-ns flex-wrap pv2 fw6">
          <div className="w-30"></div>
          <div className="w-70">Balance: {toDollars(balance_due)}</div>
        </div>
      )}
    </div>
  );
}

export default function CasesList({ cases }: { cases?: CaseData[] }) {
  return cases ? (
    <div className="bt b--light-gray pt2 mb3">
      {cases.map((caseData: CaseData, idx: number) => {
        return <Case key={idx} caseData={caseData} />;
      })}
    </div>
  ) : (
    <></>
  );
}
