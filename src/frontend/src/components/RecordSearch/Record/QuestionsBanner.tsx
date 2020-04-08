import React from 'react';
import { QuestionsData } from './types';
import { AppState } from '../../../redux/store';
import { connect } from 'react-redux';

interface Props {
  questions?: QuestionsData;
}

class QuestionsBanner extends React.Component<Props> {

  getQuestionCases() : {[caseId: string]: boolean} {
    let questionCaseIds : {[caseId: string]: boolean} = {};
    if (this.props.questions) {
        const re = /(.*)-[^-]*/;
        let res: string[] | null = [];
        let caseId: string;
        let answered: boolean;
        for (const ambiguousChargeId of Object.keys(this.props.questions)) {
            res = re.exec(ambiguousChargeId);
            caseId = res && res[1] ? res[1] : "";
            answered = ((caseId!=="") && (this.props.questions[ambiguousChargeId]["answer"] !==""));
            if (caseId !== ""){
                if(!Object.keys(questionCaseIds).includes(caseId) || questionCaseIds[caseId]) {
                    questionCaseIds[caseId] = answered;
                }
            }
        }
    }
        return questionCaseIds;
  }

  renderCases() {
      const questionCases: {[caseId: string]: boolean} = this.getQuestionCases();
      return Object.keys(questionCases).map((caseId: string)=>{
          if (questionCases[caseId]) {
              return (
                  <li className="mb2" key={"qb-"+caseId}>
                    <span className="visually-hidden">Case resolved</span>
                    <span className="fas fa-check green pr1" aria-hidden="true"></span>
                    <a className="underline" href={"#"+caseId}>{caseId}</a>
                    </li>
                )
          } else {
              return (
              <li className="mb2" key={"qb-"+caseId}>
                    <span className="fas fa-question-circle purple pr1" aria-hidden="true"></span>
                    <a className="underline" href={"#"+caseId}>{caseId}</a>
                </li>
                )
          }
    })
  }

  render() {
    if (this.props.questions && Object.keys(this.props.questions).length > 0 ) {
    return (
        <div className="bt bw3 b--light-purple bg-white shadow pa3 mb3">
            <div className="flex-lg justify-between">
                <div className="mb3 pr5-lg mb0-ns">
                    <p className="fw7 mb3">These cases need clarification before an accurate analysis can be determined</p>
                    <ul className="list">
                        {this.renderCases()}
                    </ul>
                </div>
            </div>
        </div>
        ) } else {
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

