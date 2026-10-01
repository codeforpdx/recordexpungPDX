import React from "react";
import { useAppDispatch, useAppSelector } from "../../../redux/hooks";
import {
  answerSB819Question,
  clearSB819Answer,
  selectSB819Answers,
} from "../../../redux/sb819AnswersSlice";
import { Answer, QuestionData } from "./types";

interface Props {
  question: QuestionData;
  target: string;
}

/** One yes/no question in the form RecordSponge's own eligibility questions take. */
export default function Question({ question, target }: Props) {
  const dispatch = useAppDispatch();
  const answer = useAppSelector(selectSB819Answers)[target];

  return (
    <fieldset className="relative mb3">
      <legend className="fw7 mb2">{question.text}</legend>
      <div className="radio">
        {(["yes", "no"] as Answer[]).map((value) => {
          const id = `${target}-${value}`;
          return (
            <div className="dib" key={value}>
              <input
                type="radio"
                id={id}
                name={target}
                value={value}
                checked={answer === value}
                onChange={() =>
                  dispatch(answerSB819Question({ target, answer: value }))
                }
              />
              <label htmlFor={id}>{value === "yes" ? "Yes" : "No"}</label>
            </div>
          );
        })}
        {answer && (
          <button
            type="button"
            className="dib f6 link mid-gray hover-blue bg-transparent bn pointer underline v-top"
            onClick={() => dispatch(clearSB819Answer(target))}
          >
            Clear
          </button>
        )}
      </div>
    </fieldset>
  );
}
