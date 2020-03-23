import React from 'react';

import { CountyBalanceType } from '../SearchResults/types';
import currencyFormat from '../../service/currency-format';

interface Props {
  balances: CountyBalanceType[];
  totalBalance: number;
}

export default class CountyBalances extends React.Component<Props> {
  render() {
    const listItems = this.props.balances.map((pair: CountyBalanceType) => {
      return (
        <li className="mb2">
          <span className="break-all">{pair.county_name} </span>{' '}
          <span className="fr">{currencyFormat(pair.balance)}</span>
        </li>
      );
    });
    return (
      <div className="w-100 w-33-l ph3-l mb3">
        <h3 className="fw7 bt b--light-gray pt2 mb3">
          Balance Due by County
        </h3>
        <ul className="mw5 list">{listItems.length > 0 ? listItems : 'None'}</ul>
        <div className="mw5 bt b--light-gray pt2">
          <span className="fw6">Total</span>
          <span className="fr">{' '} {currencyFormat(this.props.totalBalance)}</span>
        </div>
      </div>
    );
  }
}
