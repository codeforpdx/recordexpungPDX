import React from "react";
import { CaseData, ChargeData } from "../Record/types";
import currencyFormat from "../../../service/currency-format";
import {
  awaiting,
  chargeIdsForCase,
  questionsAt,
  shown,
} from "./questionCollection";
import { SB819Answers } from "./resolveAnalysis";
import SB819Charge, { chargeTitle } from "./SB819Charge";
import SB819CaseQuestions from "./SB819CaseQuestions";
import { SB819AnalysisData } from "./types";

interface Props {
  aCase: CaseData;
  analysis: SB819AnalysisData;
  answers: SB819Answers;
}

const OECI_CASE_DETAIL =
  "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";

/** A conviction named and nothing more, while a question on its case still holds it. */
function ChargeLine({ charge }: { charge: ChargeData }) {
  return (
    <div className="br3 bg-white ma2 ph3 pv2" id={charge.ambiguous_charge_id}>
      <div className="flex">
        <span className="w6rem shrink-none fw7">Charge</span>
        {chargeTitle(charge)}
      </div>
    </div>
  );
}

/**
 * A case: enough to identify the prosecution, the questions answered once for it, and its
 * convictions. A conviction is listed by name alone while a case question live on it is
 * unanswered, so a conviction the record rules out shows in full at once.
 */
export default function SB819Case({ aCase, analysis, answers }: Props) {
  const {
    case_number,
    location,
    current_status,
    balance_due,
    case_detail_link,
    charges,
  } = aCase;
  const caseQuestions = questionsAt(
    analysis,
    "case",
    chargeIdsForCase(analysis, case_number)
  );

  // Matches the record view: in development the API is not behind the same origin.
  const prefix = window.location.href.includes("localhost")
    ? "http://localhost:5000"
    : "";
  const linkId = case_detail_link.substring(OECI_CASE_DETAIL.length);

  return (
    <div
      id={case_number}
      className="f6 f5-l bg-gray-blue-3 shadow br3 pa1 mb4 scroll-mt-20"
    >
      <div className="cf pv2">
        <div className="fl ph3 pv1">
          <div className="fw7">Case</div>
          <a
            href={prefix + "/api/case_detail_page/" + linkId}
            target="_blank"
            rel="noopener noreferrer"
            className="link bb hover-blue"
          >
            {case_number}
          </a>
        </div>
        <div className="fl ph3 pv1">
          <div className="fw7">County</div>
          {location}
        </div>
        <div className="fl ph3 pv1">
          <div className="fw7">Status</div>
          {current_status}
        </div>
        <div className="fl ph3 pv1">
          <div className="fw7">Balance</div>
          {currencyFormat(balance_due)}
        </div>
      </div>

      <SB819CaseQuestions questions={shown(caseQuestions, answers)} />

      <ul className="list">
        {charges.map((charge) => {
          const heldByCase = awaiting(
            questionsAt(analysis, "case", [charge.ambiguous_charge_id]),
            answers
          );
          return (
            <li key={charge.ambiguous_charge_id}>
              {heldByCase ? (
                <ChargeLine charge={charge} />
              ) : (
                <SB819Charge
                  charge={charge}
                  analysis={analysis}
                  answers={answers}
                />
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
