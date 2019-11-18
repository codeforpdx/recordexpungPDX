import React from 'react';
import Charge from '../Charge';
import { ChargeType } from '../SearchResults/types';

interface Props {
  charges: ChargeType[];
}

export default class Charges extends React.Component<Props> {
  render() {
    const charges = this.props.charges.map((charge: ChargeType, i) => {
      return (
        <li key={i}>
          <Charge charge={charge} />
        </li>
      );
    });

    return <ul>{charges}</ul>;
  }
}
