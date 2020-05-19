import React from 'react';
import { CaseData } from './types';
import Charges from './Charges';
import CaseEditPanel from './CaseEditPanel';
import currencyFormat from '../../../service/currency-format';

interface Props {
  case: CaseData;
  dispositionWasUnknown: string[];

}
interface State {
  editing: Boolean;
  edited: Boolean;

}
export default class Cases extends React.Component<Props, State> {
  state: State = {
    editing: false,
    edited: false
  };

  render() {
    const {
      name,
      case_number,
      birth_year,
      case_detail_link,
      balance_due,
      charges,
      location,
      current_status
    } = this.props.case;
    const prefix = window.location.href.includes("localhost") ? "http://localhost:5000" : ""; // Hack so we do not have to use nginx for dev
    const case_detail_base = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=";
    const link_id = case_detail_link.substring(case_detail_base.length);
    return (
      this.state.editing ? <CaseEditPanel propogateSubmit={()=>{this.setState({editing: false})}} case={this.props.case} /> :
      <div id={case_number} className="mb3">
        <div className="cf pv2 br3 br--top shadow-case">
          <div className="fl ph3 pv1">
            <div className="fw7">Case </div>
            <a href={prefix + "/api/case_detail_page/" + link_id} target="_blank">{case_number}</a>
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

          {/*
          TODO
          <div className="inline-flex bs2-inset-gray bg-white fw6 br3 mt1">
            <span className="mid-gray bs2-r-gray pa2">Edited</span>
            <button className="mid-gray link hover-blue pa2">
              <span className="visually-hidden">Undo all edits</span>
              <span className="fas fa-undo f6" aria-hidden="true"></span>
            </button>
          </div>
          */}
          <div className="fl fr-l ph3 pv3">
            <button className="mid-gray hover-blue ph2" aria-controls="case-form" aria-expanded="true" data-reach-disclosure-button="" data-state="open"  onClick={() => {this.setState({editing: true})}}>
              <span className="visually-hidden">Edit Case</span>
              <span aria-hidden="true" className="fas fa-pen"></span>
            </button>
            <button className="mid-gray hover-blue ph2">
              <span className="visually-hidden">Add Charge</span>
              <span aria-hidden="true" className="fas fa-plus-circle"></span>
            </button>
          </div>
        </div>
        <Charges charges={charges} dispositionWasUnknown={this.props.dispositionWasUnknown} />
      </div>
    );
  }
}
