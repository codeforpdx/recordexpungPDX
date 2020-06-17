import React from "react";
import CaseBalances from "./CaseBalances";
import ChargesList from "./ChargesList";
import CountyBalances from "./CountyBalances";
import { CaseData, RecordSummaryData } from "../types";
import { downloadPdf } from "../../../../redux/search/actions";

interface Props {
  cases?: CaseData[];
  summary: RecordSummaryData;
}

export default class RecordSummary extends React.Component<Props> {
  handleDownloadClick = () => {
    downloadPdf();
  };
  render() {
    const {
      total_charges,
      eligible_charges_by_date,
      county_balances,
      total_balance_due,
      total_cases,
    } = this.props.summary;

    return (
      <div className="bg-white shadow br3 mb3 ph3 pb3">
        <div className="flex justify-between">
          <h2 className="mv3 f5 fw7">Search Summary</h2>
          <button
            onClick={this.handleDownloadClick}
            className="ma2 ba bw1 b--light-gray mid-gray bg-white link hover-blue fw6 br3 pv1 ph2"
          >
            Download as PDF
          </button>
        </div>
        <div className="flex-ns flex-wrap">
          <ChargesList
            eligibleChargesByDate={eligible_charges_by_date}
            totalCases={total_cases}
            totalCharges={total_charges}
          />
          <div className="w-100 w-33-l ph3-l mb3">
            <CaseBalances
              cases={this.props.cases}
              totalBalance={total_balance_due}
            />
            {total_balance_due > 0 && (
              <CountyBalances balances={county_balances} />
            )}
          </div>
        </div>
      </div>
    );
  }
}
