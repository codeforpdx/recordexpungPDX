import React from 'react';

import { RecordSummaryType, CountyBalanceType } from '../SearchResults/types';

interface Props {
  balances: CountyBalanceType[];
}

export default class CountyBalances extends React.Component<Props> {
  render() {
    const listItems = this.props.balances.map(((pair:CountyBalanceType) => {
      return <li className="mb2"><span className="fw6">{pair.county_name} </span> {"$" + pair.balance}</li>
    }));
    return (
      <div className="w-100 w-20-ns w-33-l pr3 mb3">
        <h3 className="fw7 bt b--light-gray pt2 mb3">Balance Due by County</h3>
        <ul className="list">
          {(listItems.length > 0 ? listItems : "Nooooooone")}
        </ul>
      </div>
      )
  }
}
