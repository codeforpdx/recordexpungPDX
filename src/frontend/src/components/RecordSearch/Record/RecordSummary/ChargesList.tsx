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
    ).map(([eligibilityDate, casesWithHeaderAndChargesNames]: [string, any[]]) => {
      const numCharges = casesWithHeaderAndChargesNames.reduce((acc: number, entry: any)=>{ return acc +entry[1].length}, 0);
      const listItems = this.buildListItems(casesWithHeaderAndChargesNames);
      const categoryHeader = this.buildCategoryHeader(eligibilityDate, numCharges, this.props.totalCharges);
      return (
        <div className="mb3" key={eligibilityDate}>
          {categoryHeader}
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

  buildListItems(casesWithHeaderAndChargesNames: any[]) {
    return casesWithHeaderAndChargesNames.map(
      (entry) => {
        const [caseHeaderWithBalance, chargesNames] = entry;
        const listItemsInCase = chargesNames.map(
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
        return (
          <>
            <li>
              {caseHeaderWithBalance}
            </li>
            {listItemsInCase}
          </>
        );
      }
    )
  }

  buildCategoryHeader(eligibilityDate: string, numCharges: number, totalNumCharges: number) {
    const SHOW_ALL_CHARGES_THRESHOLD = 20;
    const showAllCharges = totalNumCharges > SHOW_ALL_CHARGES_THRESHOLD;
    const labelColor =
        eligibilityDate === "Eligible Now"
          ? "green"
          : eligibilityDate === "Ineligible"
          ? "red"
          : eligibilityDate === "Needs More Analysis"
          ? "purple"
          : "dark-blue";
    return (
      <div className={labelColor + " bb b--light-gray lh-copy pb1"}>
        <span className="fw7 mb2"> {eligibilityDate} </span>
          <span>
            {" "}
            {numCharges  > 0 ? `(${numCharges})` : "" }{" "}
          </span>
          <p className="f6 fw5">
            {eligibilityDate === "Ineligible" &&
            !showAllCharges
              ? "Excludes traffic violations, which are always ineligible"
              : eligibilityDate === "Needs More Analysis"
              ? "These charges need clarification below before an accurate analysis can be determined"
              : ""}
          </p>
        </div>
    )
  }
}
