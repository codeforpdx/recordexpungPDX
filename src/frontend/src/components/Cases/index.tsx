import React from 'react';
import Case from '../Case';
import { CaseType } from '../SearchResults/types';

interface Props {
  cases: CaseType[];
}

export default class Cases extends React.Component<Props> {
  render() {
    console.log('cases', this.props.cases);
    const allCases = this.props.cases.map((caseInstance, index) => {
      return (
        <li key={index}>
          <Case case={caseInstance} />
        </li>
      );
    });

    return (
      <div className="mb3">
        <ul>{allCases}</ul>
      </div>
    );
  }
}
