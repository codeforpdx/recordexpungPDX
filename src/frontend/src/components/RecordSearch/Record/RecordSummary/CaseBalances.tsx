import React from "react";
import { useSelector } from "react-redux";
import BalanceList from "./BalanceList";
import { CaseData } from "../types";
import { AppState } from "../../../../redux/store";
import { selectCasesWithBalanceDue } from "../../../../redux/search/selectors";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  totalBalance: number;
}

const CaseBalances: React.FunctionComponent<Props> = (props) => {
  const cases = useSelector((state: AppState) => {
    return selectCasesWithBalanceDue(state);
  });

  const listItems = cases.map((element: CaseData) => {
    return (
      <li className="mb2" key={element.case_number}>
        <a
          className="link underline hover-blue break-all"
          href={`#${element.case_number}`}
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
        listItems={listItems}
        title="Balance Due by Case"
        totalBalance={props.totalBalance}
      />
    </div>
  );
};

export default CaseBalances;
