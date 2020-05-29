import React from 'react';
import {AnswerData, QuestionSummaryData} from './types';
import {selectAnswer} from '../../../redux/search/actions';
import store, {AppState} from '../../../redux/store';
import {connect} from 'react-redux';

interface Props {
  ambiguous_charge_id: string;
  question_summary?: QuestionSummaryData;
  loading?: boolean;
}

class Question extends React.Component<Props> {
  render() {
    if (this.props.question_summary) {
      const question_summary = this.props.question_summary;
      const handleRadioChange = (answerData: AnswerData) => {
        return (e: React.BaseSyntheticEvent) => {
          if (answerData.edit) {
            store.dispatch(selectAnswer(question_summary.ambiguous_charge_id, question_summary.case_number, e.target.value, answerData.edit))
          }
        }
      };
      const question_root = question_summary.root;
      const options: { [option: string]: any } = question_root.options;
      return (
        <div className="w-100 bl bw3 b--light-purple pa3 pb1">
          <fieldset className="relative mb4">
            <legend className="fw7 mb2">{question_root.text}</legend>
            <div className="radio">
            {Object.keys(options).map(
              (answer: string) => {
                const id: string = question_summary.ambiguous_charge_id + answer;
                return (
                  <div className="dib" key={id}>
                    <input type="radio" name={question_summary.ambiguous_charge_id} id={id} value={answer} onChange={handleRadioChange(options[answer])} defaultChecked={question_root.selection === answer} />
                    <label htmlFor={id}>{answer}</label>
                  </div>
                )
              })}
            </div>
            {(this.props.loading ?
              <div className="radio-spinner absolute" role="status">
                <span className="spinner spinner--sm mr1"></span>
                <span className="f6 fw5">Updating&#8230;</span>
              </div> :
                null
              )
            }
          </fieldset>
        </div>
      )
    } else {
      return (<></>);
    }
  }
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

