import React from 'react';
import Eligibility from './Eligibility';
import TimeEligibility from './TimeEligibility';
import TypeEligibility from './TypeEligibility';
import Questions from './Questions';
import { ChargeData } from './types';

interface Props {
  charge: ChargeData;
}

export default class Charge extends React.Component<Props> {
  render() {
    const {
      case_number,
      ambiguous_charge_id,
      date,
      disposition,
      statute,
      name,
      type_name,
      expungement_result
    } = this.props.charge;

    const dispositionEvent = (disposition: any, date: any) => {
      let dispositionEvent;
      dispositionEvent = disposition.status;
      if (disposition.status === "Convicted") {
        dispositionEvent += " - " + disposition.date;
      } else if (disposition.status === "Unrecognized") {
        dispositionEvent += " (\"" + disposition.ruling + "\")";
      } else if (disposition.status === "Unknown") {
        dispositionEvent = "Unknown";
      }
      if (disposition.amended) {
        dispositionEvent += " (Amended)"
      }
      return dispositionEvent;
    };

    const buildDisposition = (disposition: any, date: any) => {
      return (
        <li className="mb2">
          <span className="fw7">Disposition: </span> {dispositionEvent(disposition, date)}
        </li>
      );

    };

    const buildRecordTime = () => {
      if (
           (
             expungement_result.type_eligibility.status === "Eligible" ||
             expungement_result.type_eligibility.status === "Needs more analysis"
           )
           &&
           expungement_result.time_eligibility) {
        return (
          <TimeEligibility time_eligibility={expungement_result.time_eligibility} />
        );
      }
    };

    return (
      <div className="br3 ma2 bg-white" id={ambiguous_charge_id}>
        <Eligibility expungement_result={expungement_result} />
        <div className="flex-l ph3 pb3">
          <div className="w-100 w-40-l pr3">
            {buildRecordTime()}
            <TypeEligibility
              type_eligibility={expungement_result.type_eligibility}
              type_name={type_name}
            />
          </div>
          <div className="w-100 w-60-l pr3">
            <ul className="list">
              <li className="mb2">
                <span className="fw7">Charge: </span>
                {`${statute}-${name}`}
              </li>
              {buildDisposition(disposition, date)}
              <li className="mb2">
                <span className="fw7">Charged: </span> {date}
              </li>
            </ul>
          </div>
        </div>
        <Questions ambiguous_charge_id={ambiguous_charge_id}/>
      </div>
    );
  }
}
