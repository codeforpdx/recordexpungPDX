import React from 'react';
import {QuestionsData} from './types';
import {AppState} from '../../../redux/store';
import {connect} from 'react-redux';

interface Props {
  questions?: QuestionsData;
}

class QuestionsBanner extends React.Component<Props> {

  getQuestionCaseNumbers(): { [caseNumber: string]: boolean } {
    let questionCaseNumbers: { [caseNumber: string]: boolean } = {};
    if (this.props.questions) {
      let caseNumber: string;
      let answered: boolean;
      for (const ambiguousChargeId of Object.keys(this.props.questions)) {
        caseNumber = this.props.questions[ambiguousChargeId]["case_number"];
        answered = this.props.questions[ambiguousChargeId]["answer"] !== "";
        if (!Object.keys(questionCaseNumbers).includes(caseNumber) || questionCaseNumbers[caseNumber]) {
          questionCaseNumbers[caseNumber] = answered;
        }
      }
    }
    return questionCaseNumbers;
  }

  renderStatus(answered: boolean) {
    if (answered) {
      return (
        <>
          <span className="visually-hidden">Case resolved</span>
          <span className="fas fa-check green pr1" aria-hidden="true"></span>
        </>
      )
    } else {
      return (
        <span className="fas fa-question-circle purple pr1" aria-hidden="true"></span>
      )
    }
  }

  renderCases() {
    const questionCasesNumbers: { [caseNumber: string]: boolean } = this.getQuestionCaseNumbers();
    return Object.keys(questionCasesNumbers).map((caseNumber: string) => {
      return (
        <li className="mb2" key={"qb-" + caseNumber}>
          {this.renderStatus(questionCasesNumbers[caseNumber])}
          <a className="underline" href={"#" + caseNumber}>{caseNumber}</a>
        </li>
        )
    })
  }

  render() {
    if (this.props.questions && Object.keys(this.props.questions).length > 0) {
      return (
        <div className="bl bw3 b--light-purple bg-white shadow pa3 mb3">
        <div className="flex-lg justify-between">
        <div className="mb3 pr5-lg mb0-ns">
        <p className="fw7 mb3">These cases need clarification before an accurate analysis can be determined</p>
        <ul className="list">
        {this.renderCases()}
        </ul>
        </div>
        </div>
        </div>
      )
    } else {
      return <div></div>
    }
  }
}

function mapStateToProps(state: AppState, ownProps: Props) {
  return {
    questions: state.search.questions,
  };
}

export default connect(
  mapStateToProps
)(QuestionsBanner);

