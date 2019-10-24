import React from 'react';

interface Props {
  charge: {
    disposition: {
      ruling: string;
    };
  };
}

export default class Charge extends React.Component<Props> {
  render() {
    const { disposition } = this.props.charge;

    return (
      <div className="br3 ma2 bg-white">
        <h2 className="fw6 green bg-washed-green pv2 ph3 ma2 mb3 dib br3">
          Eligible now
        </h2>
        <div className="flex-l ph3 pb3">
          <div className="w-100 w-30-l pr3">
            <div className="relative mb3">
              <i
                aria-hidden="true"
                className="absolute fas fa-check-circle green"
              ></i>
              <div className="ml3 pl1">
                <span className="fw7">Time:</span> Eligible now
              </div>
            </div>
            <div className="relative mb3">
              <i
                aria-hidden="true"
                className="absolute fas fa-check-circle green"
              ></i>
              <div className="ml3 pl1">
                <span className="fw7">Type:</span> Eligible{' '}
                <span className="nowrap">137.225(5)(b)</span>
              </div>
            </div>
          </div>
          <div className="w-100 w-70-l pr3">
            <ul className="list">
              <li className="mb2">
                <span className="fw7">Charge: </span>4759924B - Poss Controlled
                Sub 2
              </li>
              <li className="mb2">
                <span className="fw7">Disposition: </span> {disposition.ruling}
              </li>
              <li className="mb2">
                <span className="fw7">Convicted: </span>2/12/1987
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
