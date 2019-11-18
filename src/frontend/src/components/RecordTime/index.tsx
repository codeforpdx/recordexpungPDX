import React from 'react';
import { ExpungementResultType } from '../SearchResults/types';

interface Props {
  expungement_result: ExpungementResultType;
}

export default class RecordTime extends React.Component<Props> {
  render() {
    const {
      time_eligibility_reason,
      time_eligibility
    } = this.props.expungement_result;

    const timeNow = (
      <div className="relative mb3">
        <i
          aria-hidden="true"
          className="absolute fas fa-check-circle green"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Time:</span> Eligible Now
        </div>
      </div>
    );

    const timeLater = (
      <div className="relative mb3">
        <i aria-hidden="true" className="absolute fas fa-clock dark-blue"></i>
        <div className="ml3 pl1">
          <span className="fw7">Time:</span> {time_eligibility_reason}
        </div>
      </div>
    );

    const time = () => {
      if (time_eligibility === true) {
        return timeNow;
      } else {
        return timeLater;
      }
    };

    return time();
  }
}
