import React from "react";
import { TypeEligibilityData } from "./types";
import { newlineOrsInString } from "./util";

interface Props {
  type_eligibility: TypeEligibilityData;
  type_name: string;
}

export default class RecordType extends React.Component<Props> {
  render() {
    const { status, reason } = this.props.type_eligibility;

    const eligible = (reason: string) => (
      <div className="relative mb3 connect connect-type">
        <i aria-hidden="true" className="absolute fas fa-circle z-1"></i>
        <div className="ml3 pl1">
          {newlineOrsInString(<span className="fw7">Type: </span>, reason)}
        </div>
      </div>
    );

    const review = (
      <div className="relative mb3 connect connect-type">
        <i
          aria-hidden="true"
          className="absolute fas fa-question-circle purple bg-white z-1"
        ></i>
        <div className="ml3 pl1">
          {newlineOrsInString(<span className="fw7">Type: </span>, reason)}
        </div>
      </div>
    );

    const ineligible = (reason: string) => (
      <div className="relative mb3 connect connect-type">
        <i
          aria-hidden="true"
          className="absolute fas fa-times-circle red bg-white z-1"
        ></i>
        <div className="ml3 pl1">
          {newlineOrsInString(<span className="fw7">Type: </span>, reason)}
        </div>
      </div>
    );

    if (status === "Eligible") {
      return eligible(reason);
    } else if (status === "Needs More Analysis") {
      return review;
    } else if (status === "Ineligible") {
      return ineligible(reason);
    } else {
      return "Unknown type eligibility";
    }
  }
}
