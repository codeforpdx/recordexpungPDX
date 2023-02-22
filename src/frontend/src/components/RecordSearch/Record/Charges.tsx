import React from "react";
import Charge from "./Charge";
import { ChargeData } from "./types";

interface Props {
  charges: ChargeData[];
  showEditButtons: boolean;
  whenEditing: Function;
  whenDoneEditing: Function;
}

export default class Charges extends React.Component<Props> {
  render() {
    const charges = this.props.charges.map((charge: ChargeData, i) => {
      return (
        <li
          key={charge.ambiguous_charge_id}
          id={"scroll-spy-trigger_charge_" + charge.ambiguous_charge_id}
        >
          <Charge
            charge={charge}
            editing={false}
            isNewCharge={false}
            showEditButtons={this.props.showEditButtons}
            whenEditing={() => {
              this.props.whenEditing();
            }}
            whenDoneEditing={() => {
              this.props.whenDoneEditing();
            }}
          />
        </li>
      );
    });

    return <ul className="list">{charges}</ul>;
  }
}
