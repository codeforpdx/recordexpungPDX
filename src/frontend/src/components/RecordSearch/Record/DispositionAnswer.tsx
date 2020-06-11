import React from "react";
import { QuestionData } from "./types";
import store from "../../../redux/store";

interface Props {
  question: QuestionData;
  selectFunction: Function;
  answer: string;
  questionState: any;
  setQuestionState: any;
}

export function DispositionAnswer(props: Props) {
  const answerId = props.question.question_id + props.answer;
  const answerData = props.question.options[props.answer];
  const isChecked = props.questionState.dispositionAnswer === props.answer;

  function handleOptionRequiringTextInputFollowUp() {
    return props.setQuestionState((questionState: any) => {
      return {
        ...questionState,
        dispositionAnswer: props.answer,
      };
    });
  }

  function handleOtherDisposition() {
    props.setQuestionState((questionState: any) => {
      return {
        ...questionState,
        dispositionAnswer: props.answer,
      };
    });
    return store.dispatch(
      props.selectFunction(
        props.question.question_id,
        props.answer,
        answerData.edit || {},
        "06/01/2020"
      )
    );
  }

  function onChangeHandler() {
    switch (props.answer) {
      case "Convicted":
      case "Probation Revoked":
        return handleOptionRequiringTextInputFollowUp();
      case "Dismissed":
      case "Unknown":
        return handleOtherDisposition();
    }
  }

  return (
    <div className="dib" key={"div-" + answerId}>
      <input
        type="radio"
        name={props.question.question_id}
        id={"radio-" + answerId}
        value={props.answer}
        onChange={onChangeHandler}
        checked={isChecked}
      />
      <label htmlFor={"radio-" + answerId}>{props.answer}</label>
    </div>
  );
}
