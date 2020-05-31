import {Answer} from "./Answer";
import React from "react";
import {QuestionData} from "./types";

interface Props {
  question: QuestionData,
  selectFunction: Function,
}

export function Question(props: Props) {
  const render = () => {
    return (
      <fieldset className="relative mb4">
        <legend className="fw7 mb2">{props.question.text}</legend>
        <div className="radio">
        {Object.keys(props.question.options).map((answer: string) => {
            const id = props.question.question_id + answer;
            return (
              <Answer key={id} question={props.question} selectFunction={props.selectFunction} answer={answer} />
            );
          }
        )}
        </div>
      </fieldset>
    )
  };
  return render();
}