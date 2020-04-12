import React from 'react';
import {QuestionData} from './types';
import {selectAnswer} from '../../../redux/search/actions';
import store, {AppState} from '../../../redux/store';
import {connect} from 'react-redux';

interface Props {
  ambiguous_charge_id: string;
  question?: QuestionData;
  loading?: boolean;
}

class Question extends React.Component<Props> {

  handleRadioChange = (e: React.BaseSyntheticEvent) => {
    store.dispatch(selectAnswer(e.target.name, e.target.value))
  };

  render() {
    if (this.props.question) {
      const options: { [option: string]: string } = this.props.question.options;
      return (
        <div className="w-100 bt bw3 b--light-purple pa3 pb1">
          <fieldset className="relative mb4">
            <legend className="fw7 mb2">{this.props.question.question}</legend>
            <div className="radio">
            {Object.keys(options).map(
              (option_str: string) => {
                const id: string = this.props.ambiguous_charge_id + options[option_str];
                return (
                  <div className="dib" key={id}>
                  <input type="radio" name={this.props.ambiguous_charge_id} id={id} value={options[option_str]} onChange={this.handleRadioChange}/>
                  <label htmlFor={id}>{option_str}</label>
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
  let question: QuestionData;
  if (state.search.questions &&
    state.search.questions[ownProps.ambiguous_charge_id]) {
    question = state.search.questions[ownProps.ambiguous_charge_id];
    return {
      ambiguous_charge_id: ownProps.ambiguous_charge_id,
      question: question,
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

