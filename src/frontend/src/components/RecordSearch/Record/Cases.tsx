import React from 'react';
import Case from './Case';
import { CaseData } from './types';

interface Props {
  cases: CaseData[];
  dispositionWasUnknown: string[];
}

export default class Cases extends React.Component<Props> {
  render() {
    const allCases = this.props.cases.map((caseInstance, index) => {
      return (
        <li key={index}>
          <Case case={caseInstance} dispositionWasUnknown={this.props.dispositionWasUnknown} />
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
