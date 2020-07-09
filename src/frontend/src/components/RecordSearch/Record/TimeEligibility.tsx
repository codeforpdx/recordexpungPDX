import React from "react";
import { TimeEligibilityData } from "./types";

interface Props {
  time_eligibility: TimeEligibilityData;
}

export default class TimeEligibility extends React.Component<Props> {
  render() {
    const { status, reason } = this.props.time_eligibility;

    const timeNow = (
      <div className="relative mb3 connect connect-time">
        <i
          aria-hidden="true"
          className="absolute fas fa-check-circle green bg-white z-1"
        ></i>
        <div className="ml3 pl1">
          <span className="fw7">Time</span> Eligible Now
        </div>
      </div>
    );

    const timeLater = (reason: string) => (
      <div className="relative mb3 connect connect-time">
        <i aria-hidden="true" className="absolute fas fa-clock dark-blue bg-white z-1"></i>
        <div className="ml3 pl1">
          <span className="fw7">Time</span> {reason}
        </div>
      </div>
    );

    const time = () => {
      if (status === "Eligible") {
        return timeNow;
      } else {
        return timeLater(reason);
      }
    };

    return time();
  }
}
