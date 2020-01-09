import React from 'react';
import Eligibility from '../Eligibility';
import RecordTime from '../RecordTime';
import RecordType from '../RecordType';
import { ChargeType } from '../SearchResults/types';

interface Props {
  charge: ChargeType;
}

export default class Charge extends React.Component<Props> {
  render() {
    const {
      date,
      disposition,
      statute,
      name,
      type_name,
      expungement_result
    } = this.props.charge;


    const knownDisposition = (disposition: any, date: any) => {
      let dispositionEvent = disposition.status;
      if (disposition.status === "Convicted") {
        dispositionEvent += " - " + disposition.date;
      } else if (disposition.status === "Unrecognized") {
        dispositionEvent += " (\"" + disposition.ruling + "\")";
      }
      return <>
        <li className="mb2">
          <span className="fw7">Disposition:</span> {dispositionEvent}
        </li>
        <li className="mb2">
          <span className="fw7">Arrested: </span> {date}
        </li>
      </>
    };

    const dispositionRender = (disposition: any, date: any) => {
      if (disposition === null) {
        return (
          <li className="mb2">
            <span className="fw7">Disposition: </span> Missing
          </li>
        );
      } else {
        return knownDisposition(disposition, date);
      }
    };

    const recordTimeRender = () => {
      if (expungement_result.time_eligibility) {
        return (
          <RecordTime time_eligibility={expungement_result.time_eligibility} />
        );
      }
    };

    return (
      <div className="br3 ma2 bg-white">
        <Eligibility expungement_result={expungement_result} />
        <div className="flex-l ph3 pb3">
          <div className="w-100 w-40-l pr3">
            {recordTimeRender()}
            <RecordType
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
              {dispositionRender(disposition, date)}
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
