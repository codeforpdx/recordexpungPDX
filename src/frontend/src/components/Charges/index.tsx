import React from 'react';
import Charge from '../Charge';
import { ChargeType } from '../SearchResults/types';

interface Props {
  charges: ChargeType[];
}

export default class Charges extends React.Component<Props> {
  render() {
    console.log('mapping', this.props.charges);
    const charges = this.props.charges.map((charge: ChargeType, i) => {
      console.log('charge', charge);
      return (
        <li key={i}>
          <Charge charge={charge} />
        </li>
      );
    });

    return <ul>{charges}</ul>;
  }
}
