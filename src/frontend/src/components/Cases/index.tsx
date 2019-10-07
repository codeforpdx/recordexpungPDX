import React from 'react';
import Case from '../Case';

interface Props {
  cases: any[];
}

export default class Cases extends React.Component<Props> {
  render() {
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
