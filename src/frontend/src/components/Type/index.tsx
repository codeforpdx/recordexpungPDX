import React from 'react';

interface Props {
  expungement_result: any;
}

export default class Type extends React.Component<Props> {
  render() {
    const {
      type_eligibility,
      type_eligibility_reason,
      time_eligibility
    } = this.props.expungement_result;

    const eligible = (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-check-circle green"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> Eligible{' '}
          <span className="nowrap">{type_eligibility_reason}</span>
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
          <span className="nowrap">{type_eligibility_reason}</span>
        </div>
      </div>
    );

    const type = () => {
      if (type_eligibility === true) {
        return eligible;
      } else if (type_eligibility === 'None') {
        return review;
      } else if (time_eligibility === false) {
        return ineligible;
      }
      return 'error';
    };

    return type();
  }
}
