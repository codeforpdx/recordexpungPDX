import React from 'react';
import Charge from '../Charge';

interface Props {
  charges: any[];
}

export default class Charges extends React.Component<Props> {
  render() {
    const charges = this.props.charges.map((charge, i) => {
      return (
        <li key={i}>
          <Charge charge={charge} />
        </li>
      );
    });

    return <ul>{charges}</ul>;
  }
}
