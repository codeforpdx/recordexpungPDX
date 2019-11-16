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

    console.log('HIII NPW', this.props.expungement_result);

    const eligible = (
      <div className="ml3 pl1">
        <span className="fw7">Type:</span> Eligible{' '}
        <span className="nowrap">{type_eligibility_reason}</span>
      </div>
    );

    const review = (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-question-circle purple"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Type:</span> {type_eligibility_reason}
        </div>
      </div>
    );

    const ineligible = (
      <div className="ml3 pl1">
        <span className="fw7">Type:</span> Ineligible{' '}
        <span className="nowrap">{type_eligibility_reason}</span>
      </div>
    );

    const type = () => {
      console.log('Type_eligibility:', type_eligibility);
      if (type_eligibility === true) {
        return eligible;
      } else if (time_eligibility === null) {
        return review;
      } else {
        return ineligible;
      }
    };

    return type();
  }
}
