import React from "react";
import { CountyFilingFeeData } from "../types";
import currencyFormat from "../../../../service/currency-format";

interface Props {
  county_filing_fees: CountyFilingFeeData[];
  total_filing_fees_due: number;
}

export default class CountyFines extends React.Component<Props> {
  render() {
    const perCaseFilingFee = 281;
    return (
      <div className="mb4">
        <h3 className="fw7 bt b--light-gray pt2 mb3">
          Filing costs by county{" "}
          <a className=" gray link hover-blue underline" href="/manual#file">
            <i
              aria-hidden="true"
              className="fas fa-question-circle link hover-dark-blue"
            ></i>
            <span className="visually-hidden">
              Learn more about filing fees
            </span>
          </a>
        </h3>
        {this.props.county_filing_fees.map(
          (case_filing_fee: CountyFilingFeeData) => {
            return (
              <>
                <h4 className="fw6 mb2">{case_filing_fee.county_name}</h4>
                <ul className="mw5 list mb3">
                  <li className="mb2">
                    <span className="link hover-blue">{`Case Conviction x${case_filing_fee.cases_with_eligible_convictions}`}</span>{" "}
                    <span className="fr">
                      {currencyFormat(
                        perCaseFilingFee *
                          case_filing_fee.cases_with_eligible_convictions
                      )}
                    </span>
                  </li>
                  <li className="mb2">
                    <span className="link hover-blue">Fingerprint Fee</span>{" "}
                    <span className="fr">$80.00</span>
                  </li>
                </ul>
              </>
            );
          }
        )}
        <div className="mw5 bt b--light-gray pt2">
          <span className="fw6">Total</span>
          <span className="fr">
            {currencyFormat(this.props.total_filing_fees_due)}
          </span>
        </div>
      </div>
    );
  }
}
