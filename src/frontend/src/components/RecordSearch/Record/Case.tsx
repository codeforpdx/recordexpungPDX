import React from "react";
import { CaseData } from "./types";
import Charges from "./Charges";
import currencyFormat from "../../../service/currency-format";

interface Props {
  case: CaseData;
}

export default class Cases extends React.Component<Props> {
  render() {
    const {
      name,
      case_number,
      birth_year,
      case_detail_link,
      balance_due,
      charges,
      location,
      current_status,
    } = this.props.case;
    let ineligibleCharges = 0; 
    let allIneligible = 0
    for (let i = 0; i < charges.length; i++){ 
      let typeEligibility = charges[i].expungement_result.type_eligibility.status
      if (typeEligibility == "Ineligible") {
        ineligibleCharges++
      }
    }
    if (ineligibleCharges == charges.length) {
        allIneligible=1
      }
    const prefix = window.location.href.includes("localhost")
      ? "http://localhost:5000"
      : ""; // Hack so we do not have to use nginx for dev
    const case_detail_base =
      "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";
    const link_id = case_detail_link.substring(case_detail_base.length);
    return (
      <div id={case_number} className="mb3">
        <div className="cf pv2 br3 br--top shadow-case">
          <div className="fl ph3 pv1">
            <div className="fw7">Case </div>
            <a
              href={prefix + "/api/case_detail_page/" + link_id}
              target="_blank"
              className="link bb hover-blue"
            >
              {case_number}
            </a>
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">Status </div>
            {current_status}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">County </div>
            {location}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">Balance </div>
            {currencyFormat(balance_due)}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">Name </div>
            {name}
          </div>
          <div className="fl ph3 pv1">
            <div className="fw7">DOB </div>
            {birth_year}
          </div>
        </div>
        {
          balance_due > 0 && !allIneligible?
        <div className="bg-washed-red fw6 br3 pv2 ph3 ma2">Charges are ineligible until balance is paid 
        </div>:""}
        <Charges charges={charges} />
      </div>
    );
  }
}
