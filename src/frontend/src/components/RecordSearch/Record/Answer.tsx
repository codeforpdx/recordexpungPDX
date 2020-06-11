import React from 'react';
import { QuestionData } from './types';
import store from '../../../redux/store';

interface Props {
  question: QuestionData;
  selectFunction: Function;
  answer: string;
}

export function Answer(props: Props) {
  const answerId = props.question.question_id + props.answer;
  const answerData = props.question.options[props.answer];
  const isChecked = props.question.selection === props.answer;

  function handleRadioChange() {
    return store.dispatch(
      props.selectFunction(
        props.question.question_id,
        props.answer,
        answerData.edit || {}
      )
    );
  }

  return (
    <div className="dib" key={'div-' + answerId}>
      <input
        type="radio"
        name={props.question.question_id}
        id={'radio-' + answerId}
        value={props.answer}
        onChange={handleRadioChange}
        checked={isChecked}
      />
      <label htmlFor={'radio-' + answerId}>{props.answer}</label>
    </div>
  );
}
