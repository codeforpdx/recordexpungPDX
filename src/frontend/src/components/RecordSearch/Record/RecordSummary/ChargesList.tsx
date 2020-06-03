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
      const labelColor = (eligibilityDate==="Eligible now" ? "green" : eligibilityDate==="Ineligible" ? "red" : eligibilityDate==="Need more analysis" ? "purple" : "dark-blue");
      if (eligibilityDate==="Need more analysis" && listItems.length == 0) {
        return (<></>);
      } else {
        return (
          <div key={index}>
            <div className="mb1">
              <span className={"fw7 ttc mb2 " + labelColor}> {eligibilityDate} </span>
              <span> {(chargesNames.length > 0 ? `(${chargesNames.length})` : "" )} </span>
            </div>
            <p className="f6 mb2">{
              eligibilityDate==="Ineligible" ? "Excludes traffic violations, which are always ineligible" :
              eligibilityDate==="Need more analysis" ? "These charges need clarification before an accurate analysis can be determined" :
              ""}</p>
            <ul className="list mb3">
             {listItems.length > 0 ? listItems : "None"}
            </ul>
          </div>
        )
      }
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
            <li key={"chargeItem" + index} className="bt b--light-gray pt1 mb2"><a href={"#" + chargeName[0]} className="link hover-blue">{chargeName[1]}</a></li>
        )
      }));
    return listItems;
  }
}
