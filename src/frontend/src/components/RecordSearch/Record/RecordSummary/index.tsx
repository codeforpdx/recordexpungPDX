import React from "react";
import { connect } from "react-redux";
import ChargesList from "./ChargesList";
import CountyFines from "./CountyFines";
import CountyFilingFees from "./CountyFilingFees";
import { AppState } from "../../../../redux/store";
import { RecordSummaryData } from "../types";
import { downloadPdf } from "../../../../redux/search/actions";
import history from "../../../../service/history";

interface Props {
  downloadPdf: Function;
  loadingPdf?: boolean;
  summary: RecordSummaryData;
}

interface State {
  cantGenerateForms: boolean;
}

class RecordSummary extends React.Component<Props, State> {
  state = {
    cantGenerateForms: false,
  };
  handleDownloadClick = () => {
    this.props.downloadPdf();
  };

  handleGenerateFormsClick = () => {
    if (
      this.props.summary.eligible_charges_by_date["Eligible Now"] &&
      this.props.summary.eligible_charges_by_date["Eligible Now"].length > 0
    ) {
      history.push("/fill-expungement-forms");
    } else {
      this.setState({ cantGenerateForms: true });
    }
  };
  render() {
    const {
      total_charges,
      eligible_charges_by_date,
      county_fines,
      total_fines_due,
      county_filing_fees,
      total_filing_fees_due,
      total_cases,
      no_fees_reason,
    } = this.props.summary;
    return (
      <div className="bg-white shadow br3 mb3 ph3 pb3">
        <div className="flex flex-wrap justify-end mb1">
          <h2 className="f5 fw7 mv3 mr-auto">Search Summary</h2>
          {this.state.cantGenerateForms && (
            <span className="bg-washed-red mv2 pa2 br3 fw6" role="alert">
              There must be eligible charges to generate paperwork.{" "}
              <button
                onClick={() => {
                  this.setState({ cantGenerateForms: false });
                }}
              >
                <span className="visually-hidden">Close</span>
                <i aria-hidden="true" className="fas fa-times-circle gray"></i>
              </button>
            </span>
          )}
          <button
            className="ma2 nowrap mid-gray link hover-blue fw6 br3 pv1 ph2"
            onClick={this.handleGenerateFormsClick}
          >
            <i aria-hidden="true" className="fas fa-bolt pr2"></i>Generate
            Paperwork
          </button>
          <button
            className={`ma2 nowrap mid-gray link hover-blue fw6 br3 pv1 ph2${
              this.props.loadingPdf ? " loading-btn" : ""
            }`}
            onClick={this.handleDownloadClick}
          >
            <i aria-hidden="true" className="fas fa-download pr2"></i>Summary
            PDF
          </button>
        </div>

        <div className="flex-ns flex-wrap">
          <ChargesList
            eligibleChargesByDate={eligible_charges_by_date}
            totalCases={total_cases}
            totalCharges={total_charges}
          />
          <div className="w-100 w-33-l ph3-l mb3">
            <CountyFines
              all_counties_fines={county_fines}
              total_fines_due={total_fines_due}
            />
            <CountyFilingFees
              county_filing_fees={county_filing_fees}
              total_filing_fees_due={total_filing_fees_due}
              no_fees_reason={no_fees_reason}
            />
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
