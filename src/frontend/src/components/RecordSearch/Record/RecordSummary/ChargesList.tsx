import React from "react";

interface Props {
  eligibleChargesByDate: { [label: string]: any[] };
  totalCases: number;
  totalCharges: number;
}

export default class ChargesList extends React.Component<Props> {
  render() {
    const summarizedCharges = Object.entries(
      this.props.eligibleChargesByDate
    ).map(
      (
        [eligibilityDate, casesWithHeaderAndChargesNames]: [string, any[]],
        summaryIdx
      ) => {
        const numCharges = casesWithHeaderAndChargesNames.reduce(
          (acc: number, entry: any) => acc + entry[1].length,
          0
        );
        const listItems = this.buildListItems(
          casesWithHeaderAndChargesNames,
          summaryIdx
        );
        const categoryHeader = this.buildCategoryHeader(
          eligibilityDate,
          numCharges
        );
        return (
          <div className="mb3" key={eligibilityDate}>
            {categoryHeader}
            <ul className="list">{listItems}</ul>
          </div>
        );
      }
    );

    return (
      <div className="w-100 w-two-thirds-l">
        <h3 className="bt b--light-gray pt2 mb3">
          <span className="fw7">Cases</span> ({this.props.totalCases})
        </h3>
        <h3 className="bt b--light-gray pt2 mb3">
          <span className="fw7">Charges</span> ({this.props.totalCharges})
          <p className="f6 fw5 pt1">Excludes traffic violations</p>
        </h3>
        {summarizedCharges}
      </div>
    );
  }

  buildListItems(casesWithHeaderAndChargesNames: any[], summaryIdx: number) {
    return casesWithHeaderAndChargesNames.map((entry, groupIdx) => {
      const [caseHeaderWithBalance, chargesNames] = entry;
      const listItemsInCase = chargesNames.map(
        ([id, chargeName]: [string, string], index: number) => {
          return (
            <li
              key={"chargeItem" + summaryIdx + "-" + groupIdx + "-" + index}
              className="f6 bb b--light-gray pv2"
            >
              <a
                href={"#" + id}
                className={
                  caseHeaderWithBalance !== "" ? "ml2" : "link hover-blue"
                }
              >
                {chargeName}
              </a>
            </li>
          );
        }
      );
      if (caseHeaderWithBalance) {
        return [<li className="fw7 pt2">{caseHeaderWithBalance}</li>].concat(
          listItemsInCase
        );
      } else {
        return listItemsInCase;
      }
    });
  }

  buildCategoryHeader(eligibilityDate: string, numCharges: number) {
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
        <span> {numCharges > 0 ? `(${numCharges})` : ""} </span>
        <p className="f6 fw5">
          {eligibilityDate === "Needs More Analysis"
            ? "These charges need clarification below before an accurate analysis can be determined"
            : ""}
        </p>
      </div>
    );
  }
}
