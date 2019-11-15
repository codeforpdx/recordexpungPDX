import React from 'react';
import { TimeEligibility } from '../SearchResults/types';

interface Props {
  time_eligibility: TimeEligibility;
}

export default class RecordTime extends React.Component<Props> {
  render() {
    const { status, reason } = this.props.time_eligibility;

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

    const timeLater = (reason: string) => (
      <div className="relative mb3">
        <i aria-hidden="true" className="absolute fas fa-clock dark-blue"></i>
        <div className="ml3 pl1">
          <span className="fw7">Time:</span> {reason}
        </div>
      </div>
    );

    const time = () => {
      if (status === 'Eligible') {
        return timeNow;
      } else {
        return timeLater(reason);
      }
    };

    return time();
  }
}
