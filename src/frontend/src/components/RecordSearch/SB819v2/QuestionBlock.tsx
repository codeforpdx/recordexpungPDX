import React from "react";
import { Question as QuestionModel } from "./questions";
import Question from "./Question";

/** A panel's questions in the purple-barred block RecordSponge's own questions sit in. */
export default function QuestionBlock({
  questions,
}: {
  questions: QuestionModel[];
}) {
  if (questions.length === 0) return null;
  return (
    <div className="w-100 relative bl bw3 b--light-purple pa3 pb1">
      {questions.map(({ criterion, target }) => (
        <Question key={target} question={criterion.question!} target={target} />
      ))}
    </div>
  );
}
