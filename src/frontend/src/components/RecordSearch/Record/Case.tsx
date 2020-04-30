import React from 'react';
import { CaseData } from './types';
import Charges from './Charges';
import currencyFormat from '../../../service/currency-format';

interface Props {
  case: CaseData;
  dispositionWasUnknown: string[];
}

export default class Cases extends React.Component<Props> {
  render() {
    const {
      name,
      case_number,
      birth_year,
      balance_due,
      charges,
      location
    } = this.props.case;
    return (
      <div id={case_number} className="mb3">
        <div className="cf pv2 br3 br--top shadow-case">
          <div className="fl ph3 pv1">
            <div className="fw7">Case </div>
            {case_number}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">County </div>
            {location}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">Balance </div>
            {currencyFormat(balance_due)}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">Name </div>
            {name}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">DOB </div>
            {birth_year}
          </div>
        </div>
        <Charges charges={charges} dispositionWasUnknown={this.props.dispositionWasUnknown} />
      </div>
    );
  }
}
