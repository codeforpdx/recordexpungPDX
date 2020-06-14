import React from "react";
import BalanceList from "./BalanceList";
import { CaseData } from "../types";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  cases?: CaseData[];
  totalBalance: number;
}

const hasBalanceDue = (element: CaseData) => {
  return element.balance_due > 0;
};

export default class CaseBalances extends React.Component<Props> {
  render() {
    if (!this.props.cases) {
      return null;
    }

    const listItems = this.props.cases
      .filter(hasBalanceDue)
      .map((element: CaseData, i: number) => {
        return (
          <li className="mb2" key={i}>
            <a
              className="link underline hover-blue break-all"
              href={`#${element.case_number}-1`}
            >
              {element.case_number}
            </a>{" "}
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
          totalBalance={this.props.totalBalance}
        />
      </div>
    );
  }
}
