import React from 'react';
import { ExpungementResultType } from '../SearchResults/types';

interface Props {
  expungement_result: ExpungementResultType;
}

export default class RecordType extends React.Component<Props> {
  render() {
    const {
      type_eligibility,
      type_eligibility_reason
    } = this.props.expungement_result;

    const eligible = (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-check-circle green"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> Eligible{' '}
          <span className="nowrap">({type_eligibility_reason})</span>
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
          <span className="fw7">Type:</span> List B
        </div>
      </div>
    );

    const ineligible = (
      <div className="relative mb3">
        <i aria-hidden="true" className="absolute fas fa-times-circle red"></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> Ineligible{' '}
          <span className="nowrap">({type_eligibility_reason})</span>
        </div>
      </div>
    );

    if (type_eligibility === true) {
      return eligible;
    } else if (type_eligibility === null) {
      return review;
    } else if (type_eligibility === false) {
      return ineligible;
    } else {
      return 'Unknown type eligibility';
    }
  }
}
