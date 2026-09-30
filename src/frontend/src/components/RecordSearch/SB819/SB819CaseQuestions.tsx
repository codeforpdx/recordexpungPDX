import React from "react";
import { Question } from "./questionCollection";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";

/**
 * The questions that are facts about a prosecution rather than about one conviction,
 * answered once for the case so two convictions on it cannot disagree.
 */
export default function SB819CaseQuestions({
  questions,
}: {
  questions: Question[];
}) {
  if (questions.length === 0) return null;
  return (
    <div className="bg-white br3 mh2 mb2">
      <SB819QuestionBlock>
        {questions.map(({ criterion, target }) => (
          <SB819Question key={target} criterion={criterion} target={target} />
        ))}
      </SB819QuestionBlock>
    </div>
  );
}
