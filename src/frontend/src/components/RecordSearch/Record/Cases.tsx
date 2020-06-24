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
        <li key={index}>
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
      <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
        <ul className="list">{allCases}</ul>
      </div>
    );
  }
}
