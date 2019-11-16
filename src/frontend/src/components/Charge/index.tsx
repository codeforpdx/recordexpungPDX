import React from 'react';
import Eligibility from '../Eligibility';
import Time from '../Time';
import Type from '../Type';

interface Props {
  charge: {
    statute: string;
    name: string;
    disposition: {
      ruling: string;
      date: string;
    };
    expungement_result: {
      type_eligibility_reason: string;
      time_eligibility: string;
    };
  };
}

export default class Charge extends React.Component<Props> {
  render() {
    const {
      disposition,
      statute,
      name,
      expungement_result
    } = this.props.charge;

    console.log('in charge', expungement_result);

    return (
      <div className="br3 ma2 bg-white">
        <Eligibility expungement_result={expungement_result} />
        <div className="flex-l ph3 pb3">
          <div className="w-100 w-30-l pr3">
            <Time expungement_result={expungement_result} />
            <div className="relative mb3">
              <i
                aria-hidden="true"
                className="absolute fas fa-check-circle green"
              ></i>
              <Type expungement_result={expungement_result} />
            </div>
          </div>
          <div className="w-100 w-70-l pr3">
            <ul className="list">
              <li className="mb2">
                <span className="fw7">Charge: </span>
                {`${statute}-${name}`}
              </li>
              <li className="mb2">
                <span className="fw7">Disposition: </span> {disposition.ruling}
              </li>
              <li className="mb2">
                <span className="fw7">Convicted: </span> {disposition.date}
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
