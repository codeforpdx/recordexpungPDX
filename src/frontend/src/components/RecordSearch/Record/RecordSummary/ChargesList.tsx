import React from "react";
import { Link } from "react-router-dom";

interface Props {
  eligibleChargesByDate: { [label: string]: any[] };
  totalCases: number;
  totalCharges: number;
}

export default class ChargesList extends React.Component<Props> {
  render() {
    const summarizedCharges = Object.entries(
      this.props.eligibleChargesByDate
    ).map(([eligibilityDate, chargesNames]: [string, any]) => {
      const listItems = this.buildListItems(chargesNames);
      const labelColor =
        eligibilityDate === "Eligible Now"
          ? "green"
          : eligibilityDate === "Ineligible"
          ? "red"
          : eligibilityDate === "Needs More Analysis"
          ? "purple"
          : "dark-blue";
      const SHOW_ALL_CHARGES_THRESHOLD = 20;
      return (
        <div className="mb3" key={eligibilityDate}>
          <div className={labelColor + " bb b--light-gray lh-copy pb1"}>
            <span className="fw7 mb2"> {eligibilityDate} </span>
            <span>
              {" "}
              {chargesNames.length > 0 ? `(${chargesNames.length})` : ""}{" "}
            </span>
            <p className="f6 fw5">
              {eligibilityDate === "Ineligible" &&
              this.props.totalCharges > SHOW_ALL_CHARGES_THRESHOLD
                ? "Excludes traffic violations, which are always ineligible"
                : eligibilityDate === "Needs More Analysis"
                ? "These charges need clarification below before an accurate analysis can be determined"
                : ""}
            </p>
          </div>
          <ul className="list">{listItems}</ul>
        </div>
      );
    });

    return (
      <div className="w-100 w-two-thirds-l">
        <h3 className="bt b--light-gray pt2 mb3">
          <span className="fw7">Cases</span> ({this.props.totalCases})
        </h3>
        <h3 className="bt b--light-gray pt2 mb3">
          <span className="fw7">Charges</span> ({this.props.totalCharges})
        </h3>
        {summarizedCharges}
      </div>
    );
  }

  buildListItems(chargesNames: any[]) {
    const listItems = chargesNames.map(
      ([id, chargeName]: [string, string], index: number) => {
        const highlightMoneyOwed = (chargeName: string) => {
          if (chargeName.includes(" - $ owed")) {
            const text = chargeName.replace(" - $ owed", "");
            return (
              <span>
                {text}
                <span className="visually-hidden">
                  Money is owed for this case
                </span>
                <span
                  aria-hidden="true"
                  className="fw6 red bg-washed-red br2 ph1 ml2"
                >
                  $
                </span>
              </span>
            );
          } else {
            return chargeName;
          }
        };
        return (
          <li key={"chargeItem" + index} className="f6 bb b--light-gray pv2">
            <a href={"#" + id} className="link hover-blue">
              {highlightMoneyOwed(chargeName)}
            </a>
          </li>
        );
      }
    );
    return listItems;
  }
}
