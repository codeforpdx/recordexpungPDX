import React from 'react';

interface Props {
  eligibleChargesByDate: string[];
  totalCases: number;
  totalCharges: number;
}

export default class ChargesList extends React.Component<Props> {
  render() {
    const summarizedCharges = this.props.eligibleChargesByDate.map(((chargeGroup:any, index:number) => {
      const eligibilityDate = chargeGroup[0];
      const chargesNames = chargeGroup[1];
      const listItems = this.buildListItems(chargesNames);
      const labelColor = (eligibilityDate==="Eligible now" ? "green" : eligibilityDate==="Ineligible" ? "red" : "dark-blue");
      return (
        <div key={index}>
          <div className="mb1">
            <span className={"fw7 ttc mb2 " + labelColor}> {eligibilityDate} </span> <span>{(chargesNames.length > 0 ? "(" + chargesNames.length + ")" : "" )}</span>
          </div>
          <p className="f6 mb2">{eligibilityDate==="Ineligible" ? "Excludes traffic violations, which are always ineligible" : ""}</p>
          <ul className="list mb3">
           {listItems}
          </ul>
        </div>
      )
    }));

    return (
      <div className="w-100 w-two-thirds-l mb3">
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Cases</span> ({this.props.totalCases})</h3>
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Charges</span> ({this.props.totalCharges})</h3>
        {summarizedCharges}
      </div>
    );
  }

  buildListItems(chargesNames: string[]) {
    const listItems = chargesNames.map(((chargeName: string, index:number) => {
        return (
            <li key={"chargeItem" + index} className="bt b--light-gray pt1 mb1">{chargeName}</li>
        )
      }));
    if (listItems.length === 0) {
      return "None";
    } else {
      return listItems;
    }

  }
}
