import React from "react";
import { AnswerData, QuestionData, QuestionSummaryData } from "./types";
import { selectAnswer } from "../../../redux/search/actions";
import { AppState } from "../../../redux/store";
import { connect } from "react-redux";
import { Question } from "./Question";
import { DispositionQuestion } from "./DispositionQuestion";

interface Props {
  ambiguous_charge_id: string;
  loading?: string;
  question_summary?: QuestionSummaryData;
}

function Questions(props: Props) {
  function select(ambiguous_charge_id: string, case_number: string) {
    return (
      question_id: string,
      answer: string,
      edit: any,
      date: string = "",
      probation_revoked_date: string = ""
    ) => {
      return selectAnswer(
        ambiguous_charge_id,
        case_number,
        question_id,
        answer,
        edit,
        date,
        probation_revoked_date
      );
    };
  }

  const render = () => {
    if (props.question_summary) {
      const question_summary = props.question_summary;
      const selectFunction = select(
        props.question_summary.ambiguous_charge_id,
        props.question_summary.case_number
      );
      return (
        <div className="w-100 bl bw3 b--light-purple pa3 pb1">
          {renderQuestions(question_summary.root, selectFunction)}
          {props.loading === props.question_summary.ambiguous_charge_id ? (
            <div className="radio-spinner" role="status">
              <span className="spinner spinner--sm mr1"></span>
              <span className="f6 fw5">Updating&#8230;</span>
            </div>
          ) : null}
        </div>
      );
    } else {
      return <></>;
    }
  };

  const renderQuestions = (
    question: QuestionData,
    selectFunction: Function
  ) => {
    return (
      <div key={question.question_id}>
        {renderQuestion(question, selectFunction)}
        {renderChildrenQuestions(question, selectFunction)}
      </div>
    );
  };

  const renderQuestion = (question: QuestionData, selectFunction: Function) => {
    if (question.text === "Choose the disposition") {
      return (
        <DispositionQuestion
          question={question}
          selectFunction={selectFunction}
        />
      );
    } else {
      return <Question question={question} selectFunction={selectFunction} />;
    }
  };

  function renderChildrenQuestions(
    question: QuestionData,
    selectFunction: Function
  ): any {
    return Object.entries(question.options).map(
      ([answer, answerData]: [string, AnswerData]) => {
        return (
          question.selection === answer &&
          answerData.question &&
          renderQuestions(answerData.question, selectFunction)
        );
      }
    );
  }

  return render();
}

function mapStateToProps(state: AppState, ownProps: Props) {
  const question_summary =
    (state.search.questions &&
      state.search.questions[ownProps.ambiguous_charge_id]) ||
    undefined;
  return {
    question_summary,
    loading: state.search.loading,
  };
}

export default connect(mapStateToProps, {
  selectAnswer: selectAnswer,
})(Questions);
