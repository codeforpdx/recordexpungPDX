import React from "react";
import { CountyFinesData, CaseFineData } from "../types";
import currencyFormat from "../../../../service/currency-format";
import { HashLink as Link } from "react-router-hash-link";

interface Props {
  county_fines: CountyFinesData[];
  total_fines_due: number;
}

export default class CountyFines extends React.Component<Props> {
  render() {
    const listItems = this.props.county_fines
      .filter((e: CountyFinesData) => e.total_fines_due)
      .map((county_fines: CountyFinesData, i: number) => {
        return (
          <div key={i}>
            <h4 className="fw6 mb2">{county_fines.county_name}</h4>
            <ul className="mw5 list mb3">
              {county_fines.case_fines.map((case_fine: CaseFineData) => {
                return (
                  <li className="mb2" key={case_fine.case_number}>
                    <Link
                      to={`#${case_fine.case_number}`}
                      className="link hover-blue"
                    >
                      {case_fine.case_number}
                    </Link>{" "}
                    <span className="fr">
                      {currencyFormat(case_fine.balance)}
                    </span>
                  </li>
                );
              })}
            </ul>
          </div>
        );
      });

    return (
      <div className="mb4">
        <h3 className="fw7 bt b--light-gray pt2 mb3">Balance due by county</h3>
        <ul className="mw5 list">
          {listItems.length > 0 ? (
            <>
              {listItems}
              <div className="mw5 bt b--light-gray pt2">
                <span className="fw6">Total</span>
                <span className="fr">
                  {currencyFormat(this.props.total_fines_due)}
                </span>
              </div>
            </>
          ) : (
            "None"
          )}
        </ul>
      </div>
    );
  }
}
