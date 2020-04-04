import React from 'react';
import CasesSummary from './CasesSummary'
import ChargesList from './ChargesList'
import CountyBalances from './CountyBalances'
import { RecordSummaryData } from '../types';

interface Props {
  summary: RecordSummaryData;
}

export default class RecordSummary extends React.Component<Props> {
  render() {
    const {
      total_charges,
      cases_sorted,
      eligible_charges,
      county_balances,
      total_balance_due,
      total_cases
    } = this.props.summary;

    return (
      <div className="bg-white shadow br3 pa3 mb3">
        <h2 className="mb3 f5 fw7">Search Summary</h2>
        <div className="flex-ns flex-wrap">
          <CasesSummary casesSorted={cases_sorted} totalCases={total_cases}/>
          <ChargesList eligibleCharges={eligible_charges} totalCharges={total_charges}/>
          <CountyBalances totalBalance = {total_balance_due} balances={county_balances}/>
        </div>
      </div>
    );
  }
}

