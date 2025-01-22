import React from "react";
import { ExpungementResultData } from "./types";

interface Props {
  expungement_result: ExpungementResultData;
  removed: boolean;
}

export default class Eligibility extends React.Component<Props> {
  render() {
    const { charge_eligibility } = this.props.expungement_result;

    const label_color = (charge_eligibility_status: string) => {
      switch (charge_eligibility_status) {
        case "Unknown":
          return "purple bg-washed-purple";
        case "Eligible Now":
          return "green bg-washed-green";
        case "Possibly Eligible":
          return "purple bg-washed-purple";
        case "Will Be Eligible":
          return "dark-blue bg-washed-blue";
        case "Possibly Will Be Eligible":
          return "purple bg-washed-purple";
        case "Ineligible":
          return "red bg-washed-red";
        case "Needs More Analysis":
          return "purple bg-washed-purple";
        case "Ineligible If Restitution Owed":
          return "purple bg-washed-purple";
            }
    };

    const eligibility = () => {
      return (
        <h2
          className={
            label_color(charge_eligibility.status) +
            " fw6 pv2 ph3 ma2 mb3 dib br3 relative outline-2-white z-1"
          }
        >
          {charge_eligibility.label}
        </h2>
      );
    };

    return eligibility();
  }
}
