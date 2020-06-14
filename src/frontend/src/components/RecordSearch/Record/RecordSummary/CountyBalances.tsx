import React from "react";
import BalanceList from "./BalanceList";
import { CountyBalanceData } from "../types";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  balances: CountyBalanceData[];
  totalBalance: number;
}

export default class CountyBalances extends React.Component<Props> {
  render() {
    const listItems = this.props.balances.map(
      (pair: CountyBalanceData, i: number) => {
        return (
          <li className="mb2" key={i}>
            <span className="break-all">{pair.county_name} </span>{" "}
            <span className="fr">{currencyFormat(pair.balance)}</span>
          </li>
        );
      }
    );

    return (
      <BalanceList
        listItems={listItems}
        title="Balance Due by County"
        totalBalance={this.props.totalBalance}
      />
    );
  }
}
