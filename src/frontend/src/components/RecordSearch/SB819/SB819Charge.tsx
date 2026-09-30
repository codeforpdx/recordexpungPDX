import React from "react";
import { ChargeData } from "../Record/types";
import ExpungementRules from "../Record/ExpungementRules";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import { collectQuestions, partitionQuestions } from "./questionCollection";
import SB819Criteria from "./SB819Criteria";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";
import SB819SetAside from "./SB819SetAside";
import { SB819AnalysisData } from "./types";

interface Props {
  charge: ChargeData;
  analysis: SB819AnalysisData;
}

export function chargeTitle({ statute, name }: ChargeData) {
  return `${statute}${statute && "-"}${name}`;
}

function describeDisposition(disposition: ChargeData["disposition"]) {
  const { status, ruling, date } = disposition;
  if (status === "Convicted" || status === "Dismissed")
    return `${status} - ${date}`;
  if (status === "Unrecognized") return `${status} ("${ruling}")`;
  return status;
}

/**
 * A conviction as the SB-819 view presents it.
 *
 * Deliberately not the record view's charge panel. Everything here is a conviction that
 * expungement cannot reach, so that view's verdict badge and its type eligibility would
 * read the same on every charge and say nothing.
 *
 * What is left is the charge itself, then its questions in the form RecordSponge's own
 * eligibility questions take, and once every question on offer is answered, the criteria
 * and the reasoning that follows from those answers. Changing an answer above changes the
 * reasoning below.
 */
export default function SB819Charge({ charge, analysis }: Props) {
  const { ambiguous_charge_id, level, date, disposition } = charge;
  const answers = useAppSelector(selectSB819Answers);
  const { asked, setAside, setAsideReason } = partitionQuestions(
    collectQuestions(analysis, "charge", [ambiguous_charge_id]),
    answers
  );
  const hasQuestions = asked.length + setAside.length > 0;
  const answered = asked.every((q) => answers[q.target]);

  return (
    <div className="relative br3 bg-white ma2" id={ambiguous_charge_id}>
      <div className="ph3 pt3 pb1">
        <ul className="list mw6">
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Charge</span>
            {chargeTitle(charge)}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Severity</span> {level}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Disposition</span>{" "}
            {describeDisposition(disposition)}
          </li>
          <li className="flex mb2">
            <span className="w6rem shrink-none fw7">Charged</span> {date}
          </li>
        </ul>
      </div>

      <ExpungementRules expungement_rules={charge.expungement_rules} />

      {hasQuestions && (
        <div className="bt b--light-gray">
          <SB819QuestionBlock>
            {asked.map(({ criterion, target }) => (
              <SB819Question
                key={target}
                criterion={criterion}
                target={target}
              />
            ))}

            <SB819SetAside
              id={`sb819-charge-set-aside-${ambiguous_charge_id}`}
              setAside={setAside}
              setAsideReason={setAsideReason}
            />
          </SB819QuestionBlock>
        </div>
      )}

      {answered && (
        <SB819Criteria analysis={analysis.charges[ambiguous_charge_id]} />
      )}
    </div>
  );
}
