import React from 'react';
import CaseNumbersList from './CaseNumbersList'

interface Props {
  casesSorted: any;
  totalCases: number;
}
export default class CasesSummary extends React.Component<Props> {
  render() {
    return (
      <div className="w-100 w-50-ns w-33-l br-ns b--light-gray pr3 mb3">
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Cases</span> ({this.props.totalCases})</h3>
        <CaseNumbersList cases={this.props.casesSorted["fully_eligible"]} title={"Eligible Now"} subheading={""} color = "green"/>
        <CaseNumbersList cases={this.props.casesSorted["partially_eligible"]} title={"Partially Eligible"} subheading={""} color = "gradient-text-green"/>
        <CaseNumbersList cases={this.props.casesSorted["fully_ineligible"]} title={"Ineligible"} subheading={"Excludes traffic violations, which are always ineligible"} color = "red"/>
      </div>
      )
    }
  }
