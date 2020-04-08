import React from 'react';
import { QuestionData } from './types';
import {selectAnswer} from '../../../redux/search/actions';
import store, { AppState } from '../../../redux/store';
import { connect } from 'react-redux';

interface Props {
  ambiguous_charge_id: string;
  question?: QuestionData;
}

class Question extends React.Component<Props> {

  handleRadioChange = (e: React.BaseSyntheticEvent) => {
    store.dispatch(selectAnswer(e.target.name, e.target.value))
  };

  render() {
    if (this.props.question) {
    const options : {[option: string] : string} = this.props.question.options;
    return (
        <div className="flex-l items-start justify-between w-100 bt bw3 b--light-purple pt3">
          <div>
            <fieldset className="mb4">
              <legend className="fw7">{this.props.question.question}</legend>
              <div className="radio">
                {Object.keys(options).map(
                  (option_str :string)=>{
                    const id : string = this.props.ambiguous_charge_id + options[option_str];
                  return (
                    <div key={id}>
                    <input
                      type="radio"
                      name={this.props.ambiguous_charge_id}
                      id={id}
                      value={options[option_str]}
                      onChange={this.handleRadioChange}
                      />
                    <label htmlFor={id}>{option_str}</label>
                    </div>
                    )
                })}
              </div>
            </fieldset>
          </div>
        </div>
      )
    } else {
      return (<div></div>);
    }
  }
}

function mapStateToProps(state: AppState, ownProps: Props) {
  let question : QuestionData;
  if (state.search.questions &&
    state.search.questions[ownProps.ambiguous_charge_id]) {
      question = state.search.questions[ownProps.ambiguous_charge_id];
      return {
        ambiguous_charge_id: ownProps.ambiguous_charge_id,
        question: question
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
    selectAnswer : selectAnswer
  }
)(Question);

