import React from 'react';

interface Props {
  eligibleCharges: string[];
  totalCharges: number;
}

export default class ChargesList extends React.Component<Props> {
  render() {

    const listItems = this.props.eligibleCharges.map(((chargeName:string, index:number) => {
      return <li className="bt b--light-gray pt1 mb1">{chargeName}</li>
    }));

    return (
      <div className="w-100 w-50-ns w-33-l br-l b--light-gray ph3-ns mb3">
        <h3 className="bt b--light-gray pt2 mb3"><span className="fw7">Charges</span> ({this.props.totalCharges})</h3>
        <div className="mb1">
          <span className="fw7 green mb2">{"Eligible Now"} </span> <span>{"(" + this.props.eligibleCharges.length + ")"}</span>
        </div>
        <ul className="list mb3">
         {(listItems.length > 0 ? listItems : "None")}
        </ul>
      </div>
      )
    }
}