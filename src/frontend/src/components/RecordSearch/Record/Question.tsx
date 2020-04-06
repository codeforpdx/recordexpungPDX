import React from 'react';
import { QuestionData } from './types';
import {selectAnswer} from '../../../redux/search/actions';
import store, { AppState } from '../../../redux/store';
import { connect } from 'react-redux';

interface Props {
  ambiguous_charge_id: string;
  question?: QuestionData;
}

interface State {
  selected_answer: string
}

class Question extends React.Component<Props, State> {

  state = {
    selected_answer: (
    this.props.question ?
    this.props.question.selected_answer :
    "")
  };

  render() {
    return ( this.props.question ?
      (
        <div>
          <div>Question</div>
          <button
            onClick={() => {
              console.log("clicked");
              store.dispatch(selectAnswer("15PK267144-1", "clicked for jordan"));
              store.dispatch(selectAnswer("900633651-1", "clicked answer"));
            }}
                type="button">
                    Alias
          </button>
          {"state: " + this.state.selected_answer}
          {"props: " + this.props.question.selected_answer}

        </div>
      ): null
      );
  }
}

function mapStateToProps(state: AppState, ownProps: Props) {
  let question : QuestionData;
  if (state.search.questions &&
    state.search.questions[ownProps.ambiguous_charge_id]) {
      question = state.search.questions[ownProps.ambiguous_charge_id];
      console.log("with question");
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

