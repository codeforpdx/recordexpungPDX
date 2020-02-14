import React from 'react';
import CaseNumbersList from './CaseNumbersList'

interface Props {
  casesSorted: any;
  totalCases: number;
}
export default class CasesSummary extends React.Component<Props> {
  render() {
    return (
      <div className="w-100 w-30-ns w-20-l br-ns b--light-gray mr3-ns pr3 mb3">
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Cases</span> {this.props.totalCases}</h3>
        <CaseNumbersList cases={this.props.casesSorted["fully_eligible"]} title={"Cases eligible now"} subheading={""} color = "green"/>
        <CaseNumbersList cases={this.props.casesSorted["partially_eligible"]} title={"Cases partially eligible"} subheading={""} color = "green"/>
        <CaseNumbersList cases={this.props.casesSorted["fully_ineligible"]} title={"Cases ineligible"} subheading={"Excludes traffic violations, which are always ineligible"} color = "red"/>
      </div>
      )
    }
  }
