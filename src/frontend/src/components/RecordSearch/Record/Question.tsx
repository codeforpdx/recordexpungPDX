import React, {useState} from 'react';
import {AnswerData, QuestionData, QuestionSummaryData} from './types';
import {selectAnswer} from '../../../redux/search/actions';
import store, {AppState} from '../../../redux/store';
import {connect} from 'react-redux';

interface Props {
  ambiguous_charge_id: string;
  question_summary?: QuestionSummaryData;
  loading?: boolean;
}

function Question(props: Props) {
  const [selectedAnswers, setSelectedAnswers] = useState<any>({});

  function handleRadioChange(ambiguous_charge_id: string, case_number: string, question_id: string, answerData: AnswerData) {
      return (e: React.BaseSyntheticEvent) => {
        const answer = e.target.value;
        setSelectedAnswers((selectedAnswers : any) => Object.assign({}, selectedAnswers, {[question_id]: answer}));
        if (answerData.edit) {
          store.dispatch(
            selectAnswer(ambiguous_charge_id, case_number, answer, answerData.edit)
          );
        }
      }
  }

  const renderQuestion = (ambiguous_charge_id: string, case_number: string, question: QuestionData) => {
    const options = question.options;
    return (
      <>
        <fieldset className="relative mb4">
          <legend className="fw7 mb2">{question.text}</legend>
          <div className="radio">
          {Object.keys(options).map(
            (answer: string) => {
              const question_id: string = ambiguous_charge_id + question.text;
              const id: string = ambiguous_charge_id + question.text + answer;
              return (
                <div className="dib" key={id}>
                  <input type="radio" name={question_id} id={id} value={answer} onChange={handleRadioChange(ambiguous_charge_id, case_number, question_id, options[answer])} defaultChecked={question.selection === answer} />
                  <label htmlFor={id}>{answer}</label>
                </div>
              )
            })}
          </div>
          {
            (props.loading ?
            <div className="radio-spinner absolute" role="status">
              <span className="spinner spinner--sm mr1"></span>
              <span className="f6 fw5">Updating&#8230;</span>
            </div> :
              null
            )
          }
        </fieldset>
        {
          renderChildrenQuestions(ambiguous_charge_id, case_number, question)
        }
      </>
    );
  };

  function renderChildrenQuestions(ambiguous_charge_id: string, case_number: string, question: QuestionData): any {
    const question_id: string = ambiguous_charge_id + question.text;
    return Object.entries(question.options).map(([answer, answerData]: [string, AnswerData]) => {
      if (selectedAnswers[question_id] === answer && answerData.question) {
        return renderQuestion(ambiguous_charge_id, case_number, answerData.question);
      } else {
        return (<></>);
      }
    });
  }

  const render = () => {
    if (props.question_summary) {
      const question_summary = props.question_summary;
      return (
        <div className="w-100 bl bw3 b--light-purple pa3 pb1">
          {renderQuestion(question_summary.ambiguous_charge_id, question_summary.case_number, question_summary.root)}
        </div>
      )
    } else {
       return (<></>);
    }
  };
  return render();
}

function mapStateToProps(state: AppState, ownProps: Props) {
  if (state.search.questions &&
    state.search.questions[ownProps.ambiguous_charge_id]) {
    let question_summary = state.search.questions[ownProps.ambiguous_charge_id];
    return {
      ambiguous_charge_id: ownProps.ambiguous_charge_id,
      question_summary: question_summary,
      loading: state.search.loading,
    };
  } else {
    return {
      ambiguous_charge_id: ownProps.ambiguous_charge_id,
    };
  }
}


export default connect(
  mapStateToProps,
  {
    selectAnswer: selectAnswer
  }
)(Question);

