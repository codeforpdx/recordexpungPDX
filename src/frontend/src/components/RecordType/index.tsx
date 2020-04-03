import React from 'react';
import { TypeEligibility } from '../SearchResults/types';

interface Props {
  type_eligibility: TypeEligibility;
  type_name: string;
}

export default class RecordType extends React.Component<Props> {
  render() {
    const { status, reason } = this.props.type_eligibility;

    const eligible = (reason: string) => (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-check-circle green"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> {this.props.type_name + ' '}
          <div>({reason})</div>
        </div>
      </div>
    );

    const review = (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-question-circle purple"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> {this.props.type_name + ' '}
          <div>({reason})</div>

        </div>
      </div>
    );

    const ineligible = (reason: string) => (
      <div className="relative mb3">
        <i aria-hidden="true" className="absolute fas fa-times-circle red"></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> {this.props.type_name + ' '}
          <div>({reason})</div>
        </div>
      </div>
    );

    if (status === 'Eligible') {
      return eligible(reason);
    } else if (status === 'Needs more analysis') {
      return review;
    } else if (status === 'Ineligible') {
      return ineligible(reason);
    } else {
      return 'Unknown type eligibility';
    }
  }
}
