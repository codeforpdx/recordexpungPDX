import React from "react";
import { ChargeData } from "../Record/types";
import ExpungementRules from "../Record/ExpungementRules";
import { awaiting, questionsAt, shown } from "./questionCollection";
import { SB819Answers } from "./resolveAnalysis";
import SB819Criteria from "./SB819Criteria";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";
import { SB819AnalysisData } from "./types";

interface Props {
  charge: ChargeData;
  analysis: SB819AnalysisData;
  answers: SB819Answers;
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

/**
 * A conviction as the SB-819 view presents it: its detail lines, then its own questions in
 * the form RecordSponge's eligibility questions take, and once every live one is answered,
 * the criteria and what follows from them. Changing an answer above changes the reasoning
 * below.
 *
 * Deliberately not the record view's charge panel. Everything here is a conviction that
 * expungement cannot reach, so that view's verdict badge would read the same on every
 * charge and say nothing.
 */
export default function SB819Charge({ charge, analysis, answers }: Props) {
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
          <SB819QuestionBlock>
            {visible.map(({ criterion, target }) => (
              <SB819Question
                key={target}
                criterion={criterion}
                target={target}
              />
            ))}
          </SB819QuestionBlock>
        </div>
      )}

      {!awaiting(questions, answers) && (
        <SB819Criteria analysis={analysis.charges[id]} />
      )}
    </div>
  );
}
