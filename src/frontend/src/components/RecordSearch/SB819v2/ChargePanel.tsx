import React from "react";
import { ChargeData } from "../Record/types";
import ExpungementRules from "../Record/ExpungementRules";
import { awaiting, questionsAt, shown } from "./questions";
import { AnalysisData, Answers } from "./types";
import QuestionBlock from "./QuestionBlock";
import Criteria from "./Criteria";

interface Props {
  charge: ChargeData;
  analysis: AnalysisData;
  answers: Answers;
}

export function chargeTitle({ statute, name }: ChargeData) {
  return `${statute}${statute && "-"}${name}`;
}

function describeDisposition({
  status,
  ruling,
  date,
}: ChargeData["disposition"]) {
  if (status === "Convicted" || status === "Dismissed")
    return `${status} - ${date}`;
  if (status === "Unrecognized") return `${status} ("${ruling}")`;
  return status;
}

/** A conviction by name alone, while a question on its case still holds it. */
export function ChargeLine({ charge }: { charge: ChargeData }) {
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
 * A conviction: its detail lines, then its own questions, and once every live one is
 * answered, the criteria and what follows from them.
 */
export default function ChargePanel({ charge, analysis, answers }: Props) {
  const id = charge.ambiguous_charge_id;
  const questions = questionsAt(analysis, "charge", [id]);
  const visible = shown(questions, answers);

  return (
    <div className="relative br3 bg-white ma2" id={id}>
      <div className="ph3 pt3 pb1">
        <ul className="list mw6">
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Charge</span>
            {chargeTitle(charge)}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Severity</span>{" "}
            {charge.level}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Disposition</span>{" "}
            {describeDisposition(charge.disposition)}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Charged</span> {charge.date}
          </li>
        </ul>
      </div>

      <ExpungementRules expungement_rules={charge.expungement_rules} />

      {visible.length > 0 && (
        <div className="bt b--light-gray">
          <QuestionBlock questions={visible} />
        </div>
      )}

      {!awaiting(questions, answers) && (
        <Criteria charge={analysis.charges[id]} />
      )}
    </div>
  );
}
