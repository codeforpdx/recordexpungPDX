import React from "react";
import BalanceList from "./BalanceList";
import { CaseData } from "../types";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  cases?: CaseData[];
}

const hasBalanceDue = (element: CaseData) => {
  return element.balance_due > 0;
};

export default class CaseBalances extends React.Component<Props> {
  render() {
    let totalBalanceDue = 0;

    if (!this.props.cases) {
      return null;
    }

    const listItems = this.props.cases
      .filter(hasBalanceDue)
      .map((element: CaseData, i: number) => {
        totalBalanceDue += element.balance_due;

        return (
          <li className="mb2" key={i}>
            <span className="break-all">{element.case_number} </span>{" "}
            <span className="fr">{currencyFormat(element.balance_due)}</span>
          </li>
        );
      });

    return (
      <div className="mb4">
        <BalanceList
          displayTotal
          listItems={listItems}
          title="Balance Due by Case"
          totalBalance={totalBalanceDue}
        />
      </div>
    );
  }
}
