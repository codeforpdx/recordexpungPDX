import React from 'react';
import { CaseProps } from '../../redux/records/types';

export default class Cases extends React.Component<CaseProps> {
  render() {
    const { name, case_number, birth_year, balance_due } = this.props.case;
    return (
      <div className="cf pv2 br3 br--top shadow-case">
        <div className="fl ph3 pv1">
          <span className="fw7">Case </span>
          <a className="underline" href="#">
            {case_number}
          </a>
        </div>
        <div className="fl ph3 pv1">
          <span className="fw7">Balance </span>
          {balance_due}
        </div>
        <div className="fl ph3 pv1">
          <span className="fw7">Name </span>
          {name}
        </div>
        <div className="fl ph3 pv1">
          <span className="fw7">DOB </span>
          {birth_year}
        </div>
      </div>
    );
  }
}
