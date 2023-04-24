import React, { useState } from "react";
import { QuestionData } from "./types";
import store from "../../../redux/store";
import { isDate } from "../../../service/validators";
import { DispositionAnswer } from "./DispositionAnswer";

interface Props {
  question: QuestionData;
  selectFunction: Function;
}

export function DispositionQuestion(props: Props) {
  const [questionState, setQuestionState] = useState<any>({
    dispositionAnswer: props.question.selection,
    conviction_date: props.question.convicted_date_string,
    probation_revoked_date: props.question.probation_revoked_date_string,
    missingFields: false,
    invalidDate: false,
  });

  function handleDateFieldChange(e: React.BaseSyntheticEvent) {
    const dateFieldName = e.target.name;
    const dateFieldValue = e.target.value;
    return setQuestionState((questionState: any) => {
      return {
        ...questionState,
        [dateFieldName]: dateFieldValue,
      };
    });
  }

  function handleSubmit(question_id: string, question: QuestionData) {
    return () => {
      const [missingFields, invalidDate] = validateForm();
      if (missingFields || invalidDate) {
        return setQuestionState((questionState: any) => {
          return {
            ...questionState,
            missingFields: missingFields,
            invalidDate: invalidDate,
          };
        });
      } else {
        setQuestionState((questionState: any) => {
          return {
            ...questionState,
            missingFields: false,
            invalidDate: false,
          };
        });
        const answerData = question.options[questionState.dispositionAnswer];
        return store.dispatch(
          props.selectFunction(
            question_id,
            questionState.dispositionAnswer,
            answerData.edit,
            questionState.conviction_date,
            questionState.probation_revoked_date
          )
        );
      }
    };
  }

  function validateForm() {
    let missingFields = false;
    if (questionState.dispositionAnswer === "Convicted") {
      missingFields = questionState.conviction_date === "";
    } else if (questionState.dispositionAnswer === "Probation Revoked") {
      missingFields =
        questionState.conviction_date === "" ||
        questionState.probation_revoked_date === "";
    }
    let invalidDate =
      ((questionState.dispositionAnswer === "Convicted" ||
        questionState.dispositionAnswer === "Probation Revoked") &&
        questionState.conviction_date.length !== 0 &&
        !isDate(questionState.conviction_date)) ||
      (questionState.probation_revoked_date.length !== 0 &&
        !isDate(questionState.probation_revoked_date));
    return [missingFields, invalidDate];
  }

  const render = () => {
    return (
      <fieldset className="relative mb4">
        <legend className="fw7 mb2">{props.question.text}</legend>
        <div className="radio">
          {Object.keys(props.question.options).map((answer: string) => {
            const id = props.question.question_id + answer;
            return (
              <DispositionAnswer
                key={id}
                question={props.question}
                selectFunction={props.selectFunction}
                answer={answer}
                questionState={questionState}
                setQuestionState={setQuestionState}
              />
            );
          })}
        </div>
        {questionState.dispositionAnswer === "Convicted" ||
        questionState.dispositionAnswer === "Probation Revoked" ? (
          <div>
            <label
              className="db fw6 mt3 mb1"
              htmlFor={props.question.question_id + "convicted"}
            >
              Date Convicted <span className="f6 fw4">mm/dd/yyyy</span>
            </label>
            <input
              value={questionState.conviction_date}
              onChange={handleDateFieldChange}
              className="w5 br2 b--black-20 pa3"
              id={props.question.question_id + "-convicted-textfield"}
              type="text"
              name="conviction_date"
            />
          </div>
        ) : null}
        {questionState.dispositionAnswer === "Probation Revoked" ? (
          <div>
            <label
              className="db fw6 mt3 mb1"
              htmlFor={props.question.question_id + "revoked"}
            >
              Date Probation Revoked <span className="f6 fw4">mm/dd/yyyy</span>
            </label>
            <input
              value={questionState.probation_revoked_date}
              onChange={handleDateFieldChange}
              className="w5 br2 b--black-20 pa3"
              id={props.question.question_id + "-revoked-textfield"}
              type="text"
              name="probation_revoked_date"
            />
          </div>
        ) : null}
        {questionState.dispositionAnswer === "Convicted" ||
        questionState.dispositionAnswer === "Probation Revoked" ? (
          <button
            className="db bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 mt3"
            onClick={handleSubmit(props.question.question_id, props.question)}
          >
            Submit
          </button>
        ) : null}
        {questionState.missingFields &&
        (questionState.dispositionAnswer === "Convicted" ||
          questionState.dispositionAnswer === "Probation Revoked") ? (
          <div role="alert">
            <p className="dib bg-washed-red fw6 br3 pa3 mt3">
              Please complete all fields
            </p>
          </div>
        ) : null}
        {questionState.invalidDate &&
        (questionState.dispositionAnswer === "Convicted" ||
          questionState.dispositionAnswer === "Probation Revoked") ? (
          <div role="alert">
            <p className="dib bg-washed-red fw6 br3 pa3 mt3">
              The date format must be MM/DD/YYYY
            </p>
          </div>
        ) : null}
      </fieldset>
    );
  };
  return render();
}
