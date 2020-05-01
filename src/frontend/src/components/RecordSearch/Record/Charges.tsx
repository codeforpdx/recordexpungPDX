import React from 'react';
import Charge from './Charge';
import { ChargeData } from './types';

interface Props {
  charges: ChargeData[];
  dispositionWasUnknown: string[];
}

export default class Charges extends React.Component<Props> {
  render() {
    const charges = this.props.charges.map((charge: ChargeData, i) => {
      const showDispositionQuestion = this.props.dispositionWasUnknown.includes(charge.ambiguous_charge_id);
      return (
        <li key={i}>
          <Charge charge={charge} showDispositionQuestion={showDispositionQuestion} />
        </li>
      );
    });

    return <ul>{charges}</ul>;
  }
}
