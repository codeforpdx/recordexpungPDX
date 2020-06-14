import React from "react";
import { connect } from "react-redux";
import CaseBalances from "./CaseBalances";
import ChargesList from "./ChargesList";
import CountyBalances from "./CountyBalances";
import { AppState } from "../../../../redux/store";
import { RecordSummaryData } from "../types";
import { downloadPdf } from "../../../../redux/search/actions";
import { Link } from "react-router-dom";

interface Props {
  downloadPdf: Function;
  loadingPdf?: boolean;
  summary: RecordSummaryData;
}

class RecordSummary extends React.Component<Props> {
  handleDownloadClick = () => {
    this.props.downloadPdf();
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
          <Link to="/fill-expungement-forms">
            <button className="ma2 ba bw1 b--light-gray mid-gray bg-white link hover-blue fw6 br3 pv1 ph2">
              Fill Expungement Forms
            </button>
          </Link>
          <button
            onClick={this.handleDownloadClick}
            className={`ma2 nowrap mid-gray link hover-blue fw6 br3 pv1 ph2${
              this.props.loadingPdf ? " loading-btn" : ""
            }`}
          >
            <i aria-hidden="true" className="fas fa-download pr2" />
            Download PDF
          </button>
        </div>
        <div className="flex-ns flex-wrap">
          <ChargesList
            eligibleChargesByDate={eligible_charges_by_date}
            totalCases={total_cases}
            totalCharges={total_charges}
          />
          <div className="w-100 w-33-l ph3-l mb3">
            <CaseBalances totalBalance={total_balance_due} />
            {total_balance_due > 0 && (
              <CountyBalances balances={county_balances} />
            )}
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  loadingPdf: state.search.loadingPdf,
});

export default connect(mapStateToProps, {
  downloadPdf: downloadPdf,
})(RecordSummary);
