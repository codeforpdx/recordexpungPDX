import React from "react";
import { useAppDispatch, useAppSelector } from "../../../redux/hooks";
import {
  answerSB819Question,
  clearSB819Answer,
  selectSB819Answers,
} from "../../../redux/sb819AnswersSlice";
import { SB819Answer, SB819CriterionResultData } from "./types";

interface Props {
  criterion: SB819CriterionResultData;
  target: string;
}

/**
 * One yes/no question, in the same form as RecordSponge's own eligibility questions.
 *
 * Answers live in the store for the session only. Nothing is written to disk, and nothing
 * is sent to the server, so this shares no machinery with the expungement questions.
 */
export default function SB819Question({ criterion, target }: Props) {
  const dispatch = useAppDispatch();
  const answers = useAppSelector(selectSB819Answers);
  const answer = answers[target];
  const question = criterion.question;

  if (!question) return null;

  const choose = (value: SB819Answer) => () =>
    dispatch(answerSB819Question({ target, answer: value }));

  return (
    <fieldset className="relative mb3">
      <legend className="fw7 mb2">{question.text}</legend>
      <div className="radio">
        {(["yes", "no"] as SB819Answer[]).map((value) => {
          const id = `${target}-${value}`;
          return (
            <div className="dib" key={value}>
              <input
                type="radio"
                id={id}
                name={target}
                value={value}
                checked={answer === value}
                onChange={choose(value)}
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
