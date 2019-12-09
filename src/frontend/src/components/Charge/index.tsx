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
      expungement_result
    } = this.props.charge;

    const knownDisposition = (disposition: any) => (
      <>
        <li className="mb2">
          <span className="fw7">Disposition: </span> {disposition.ruling}
        </li>
        <li className="mb2">
          <span className="fw7">Arrested: </span> {date}
        </li>
      </>
    );

    const dispositionRender = (disposition: any) => {
      if (disposition === null) {
        return (
          <li className="mb2">
            <span className="fw7">Disposition: </span> Unknown
          </li>
        );
      } else {
        return knownDisposition(disposition);
      }
    };

    return (
      <div className="br3 ma2 bg-white">
        <Eligibility expungement_result={expungement_result} />
        <div className="flex-l ph3 pb3">
          <div className="w-100 w-30-l pr3">
            <RecordTime expungement_result={expungement_result} />
            <RecordType expungement_result={expungement_result} />
          </div>
          <div className="w-100 w-70-l pr3">
            <ul className="list">
              <li className="mb2">
                <span className="fw7">Charge: </span>
                {`${statute}-${name}`}
              </li>
              {dispositionRender(disposition)}
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
