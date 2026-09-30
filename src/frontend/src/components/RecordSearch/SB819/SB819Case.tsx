import React from "react";
import { CaseData, ChargeData } from "../Record/types";
import currencyFormat from "../../../service/currency-format";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import {
  chargeIdsForCase,
  collectQuestions,
  partitionQuestions,
} from "./questionCollection";
import SB819Charge, { chargeTitle } from "./SB819Charge";
import SB819CaseQuestions from "./SB819CaseQuestions";
import { SB819AnalysisData, SB819ChargeAnalysisData } from "./types";

interface Props {
  aCase: CaseData;
  analysis: SB819AnalysisData;
}

const OECI_CASE_DETAIL =
  "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";

/**
 * A conviction the record itself rules out under the main criteria. Nothing about it
 * turns on an answer, so its reasoning is shown whatever is still open on its case.
 */
function ruledOutByTheRecord(charge: SB819ChargeAnalysisData) {
  return charge.main_criteria.some(
    (c) => c.outcome === "Failed" && c.question === null
  );
}

/** A conviction named and nothing more, while the case it is on still has a question open. */
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
 * A case as the SB-819 view presents it: enough to identify the prosecution, the questions
 * that are answered once for it, and its convictions.
 *
 * The case's questions come first. Until each one on offer is answered, the convictions
 * are listed by name only, so the volunteer works down the page in the order the answers
 * are needed.
 */
export default function SB819Case({ aCase, analysis }: Props) {
  const {
    case_number,
    location,
    current_status,
    balance_due,
    case_detail_link,
    charges,
  } = aCase;
  const answers = useAppSelector(selectSB819Answers);
  const questions = partitionQuestions(
    collectQuestions(analysis, "case", chargeIdsForCase(analysis, case_number)),
    answers
  );
  const caseAnswered = questions.asked.every((q) => answers[q.target]);

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

      <SB819CaseQuestions caseNumber={case_number} questions={questions} />

      <ul className="list">
        {charges.map((charge) => (
          <li key={charge.ambiguous_charge_id}>
            {caseAnswered ||
            ruledOutByTheRecord(
              analysis.charges[charge.ambiguous_charge_id]
            ) ? (
              <SB819Charge charge={charge} analysis={analysis} />
            ) : (
              <ChargeLine charge={charge} />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
