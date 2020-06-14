import React from "react";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  displayTotal?: boolean;
  listItems: any[];
  title: string;
  totalBalance: number;
}

export default class BalanceList extends React.Component<Props> {
  render() {
    const { displayTotal, listItems, title, totalBalance } = this.props;

    return (
      <>
        <h3 className="fw7 bt b--light-gray pt2 mb3">{title}</h3>
        <ul className="mw5 list">
          {listItems.length > 0 ? listItems : "None"}
        </ul>
        {displayTotal && (
          <div className="mw5 bt b--light-gray pt2">
            <span className="fw6">Total</span>
            <span className="fr">{currencyFormat(totalBalance)}</span>
          </div>
        )}
      </>
    );
  }
}
