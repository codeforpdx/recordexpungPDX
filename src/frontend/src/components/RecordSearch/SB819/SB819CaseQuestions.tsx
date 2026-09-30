import React from "react";
import { PartitionedQuestions } from "./questionCollection";
import SB819SetAside from "./SB819SetAside";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";

interface Props {
  caseNumber: string;
  questions: PartitionedQuestions;
}

/**
 * The questions that are facts about a prosecution rather than about one conviction.
 *
 * Answered once for the case, so two convictions on the same case cannot disagree about
 * whether its sentence was completed.
 */
export default function SB819CaseQuestions({ caseNumber, questions }: Props) {
  const { asked, setAside, setAsideReason } = questions;

  if (asked.length === 0 && setAside.length === 0) return null;

  return (
    <div className="bg-white br3 mh2 mb2">
      <SB819QuestionBlock>
        {asked.map(({ criterion, target }) => (
          <SB819Question key={target} criterion={criterion} target={target} />
        ))}

        <SB819SetAside
          id={`sb819-case-set-aside-${caseNumber}`}
          setAside={setAside}
          setAsideReason={setAsideReason}
        />
      </SB819QuestionBlock>
    </div>
  );
}
