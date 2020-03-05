import React from 'react';

interface Props {
  eligibleChargesByDate: string[];
  totalCharges: number;
}

export default class ChargesList extends React.Component<Props> {
  render() {
    const summarizedCharges = this.props.eligibleChargesByDate.map(((chargeGroup:any, index:number) => {
      const eligibilityDate = chargeGroup[0];
      const chargesNames = chargeGroup[1];
      const listItems = this.buildListItems(chargesNames);
      const labelColor = (eligibilityDate==="now" ? "green" : "dark-blue");
      return (
        <>
          <div key={index}>
            <span className={"fw8 mb2 " + labelColor}> {"Eligible " + eligibilityDate} </span> <span className="fw8">{(chargesNames.length > 0 ? "(" + chargesNames.length + ")" : "" )}</span>
          </div>
          <ul className="list mb3">
           {listItems}
          </ul>
        </>
      )
    }));

    return (
      <div className="w-100 w-50-ns w-33-l br-ns b--light-gray mr3-ns pr3 mb3">
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Charges</span> {this.props.totalCharges}</h3>
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
