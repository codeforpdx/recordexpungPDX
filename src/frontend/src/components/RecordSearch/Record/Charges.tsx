import React from 'react';
import Charge from './Charge';
import { ChargeData } from './types';

interface Props {
  charges: ChargeData[];
}

export default class Charges extends React.Component<Props> {
  render() {
    const charges = this.props.charges.map((charge: ChargeData, i) => {
      return (
        <li key={i}>
          <Charge charge={charge} />
        </li>
      );
    });

    return <ul>{charges}</ul>;
  }
}
