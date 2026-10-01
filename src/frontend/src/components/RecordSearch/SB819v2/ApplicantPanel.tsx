import React from "react";
import { Question } from "./questions";
import { Answers } from "./types";
import QuestionBlock from "./QuestionBlock";

interface Props {
  /** The record-scope questions that are answered or live. */
  questions: Question[];
  answers: Answers;
}

/**
 * The questions that are facts about the applicant rather than about any conviction, asked
 * once and applied to every charge. Absent while every such question waits on a
 * main-criterion question somewhere below.
 */
export default function ApplicantPanel({ questions, answers }: Props) {
  if (questions.length === 0) return null;
  const answered = questions.filter((q) => answers[q.target]).length;

  return (
    <div id="sb819-applicant-panel" className="bg-white shadow br3 mb3 ph3 pb3">
      <div className="flex flex-wrap items-center pv3">
        <h3 className="f5 fw7 mr-auto">About the applicant</h3>
        <span className="f6 gray">
          {answered} of {questions.length} answered
        </span>
      </div>
      <QuestionBlock questions={questions} />
    </div>
  );
}
