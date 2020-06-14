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
    return (
      <>
        <h3 className="fw7 bt b--light-gray pt2 mb3">{this.props.title}</h3>
        <ul className="mw5 list">
          {this.props.listItems.length > 0 ? this.props.listItems : "None"}
        </ul>
        {this.props.displayTotal && (
          <div className="mw5 bt b--light-gray pt2">
            <span className="fw6">Total</span>
            <span className="fr">
              {" "}
              {currencyFormat(this.props.totalBalance)}
            </span>
          </div>
        )}
      </>
    );
  }
}
