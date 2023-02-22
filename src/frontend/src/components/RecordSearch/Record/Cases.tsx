import React from "react";
import Case from "./Case";
import { CaseData } from "./types";

interface Props {
  cases: CaseData[];
  showEditButtons: boolean;
  whenEditing: Function;
  whenDoneEditing: Function;
}

export default class Cases extends React.Component<Props> {
  render() {
    const allCases = this.props.cases.map((caseInstance, index) => {
      return (
        <li
          key={index}
          id={"scroll-spy-trigger_case_" + caseInstance.case_number}
        >
          <Case
            case={caseInstance}
            editing={false}
            isNewCase={false}
            showEditButtons={this.props.showEditButtons}
            whenEditing={() => {
              this.props.whenEditing();
            }}
            whenDoneEditing={() => {
              this.props.whenDoneEditing();
            }}
          />
        </li>
      );
    });

    return (
      <div className="mb3">
        <ul className="list">{allCases}</ul>
      </div>
    );
  }
}
