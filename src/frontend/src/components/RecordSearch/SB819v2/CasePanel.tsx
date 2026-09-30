import React from "react";
import { CaseData } from "../Record/types";
import currencyFormat from "../../../service/currency-format";
import { awaiting, chargeIdsOnCase, questionsAt, shown } from "./questions";
import { AnalysisData, Answers } from "./types";
import QuestionBlock from "./QuestionBlock";
import ChargePanel, { ChargeLine } from "./ChargePanel";

interface Props {
  aCase: CaseData;
  analysis: AnalysisData;
  answers: Answers;
}

const OECI_CASE_DETAIL =
  "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";

/**
 * A case: enough to identify the prosecution, the questions answered once for it, and its
 * convictions. A conviction is listed by name alone while a case question live on it is
 * unanswered.
 */
export default function CasePanel({ aCase, analysis, answers }: Props) {
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
    chargeIdsOnCase(analysis, case_number)
  );
  const visible = shown(caseQuestions, answers);

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

      {visible.length > 0 && (
        <div className="bg-white br3 mh2 mb2">
          <QuestionBlock questions={visible} />
        </div>
      )}

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
                <ChargePanel
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
