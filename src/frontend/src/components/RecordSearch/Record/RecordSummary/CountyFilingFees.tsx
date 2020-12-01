import React from "react";
import { CountyFilingFeeData } from "../types";
import currencyFormat from "../../../../service/currency-format";
import { HashLink as Link } from "react-router-hash-link";

interface Props {
  county_filing_fees: CountyFilingFeeData[];
  total_filing_fees_due: number;
  no_fees_reason: string;
}

export default class CountyFines extends React.Component<Props> {
  render() {
    const perCaseFilingFee = 281;
    return (
      <div className="mb4">
        <h3 className="fw7 bt b--light-gray pt2 mb3">
          Filing costs by county{" "}
          <Link to="/manual#file" className=" gray link hover-blue underline">
            <i
              aria-hidden="true"
              className="fas fa-question-circle link hover-dark-blue"
            ></i>
            <span className="visually-hidden">
              Learn more about filing fees
            </span>
          </Link>
        </h3>
        {this.props.county_filing_fees.map(
          (case_filing_fee: CountyFilingFeeData) => {
            return (
              <>
                <h4 className="fw6 mb2">{case_filing_fee.county_name}</h4>
                <ul className="mw5 list mb3">
                  <li className="mb2">
                    {`Case Conviction x${case_filing_fee.cases_with_eligible_convictions}`}
                    <span className="fr">
                      {currencyFormat(
                        perCaseFilingFee *
                          case_filing_fee.cases_with_eligible_convictions
                      )}
                    </span>
                  </li>
                  <li className="mb2">
                    Fingerprint Fee
                    <span className="fr">$80.00</span>
                  </li>
                </ul>
              </>
            );
          }
        )}
        {this.props.county_filing_fees.filter((county: CountyFilingFeeData) => {
          return county.cases_with_eligible_convictions > 0;
        }).length > 0 ? (
          <div className="mw5 bt b--light-gray pt2">
            <span className="fw6">Total</span>
            <span className="fr">
              {currencyFormat(this.props.total_filing_fees_due)}
            </span>
          </div>
        ) : (
          <span>{this.props.no_fees_reason}</span>
        )}
      </div>
    );
  }
}
