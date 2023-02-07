import React from "react";
import moment from "moment";
import { ExpungementResultData } from "./types";

type EligibilityColor = "green" | "dark-blue" | "purple" | "red";

// Status can come from either:
// expungement_result.charge_eligibility.status or
// summary.charges_grouped_by_eligibility_and_case keys
export function getEligibilityColor(status: string, caseBalance = 0) {
  let color: EligibilityColor;
  let icon = "fa fa-";

  switch (status) {
    case "Unknown":
    case "Possible Eligible":
    case "Possibly Will Be Eligible":
    case "Needs More Analysis":
      color = "purple";
      icon += "question-circle";
      break;
    case "Ineligible":
      color = "red";
      icon += "circle-xmark";
      break;
    case "Eligible Now":
      color = caseBalance > 0 ? "dark-blue" : "green";
      icon += caseBalance > 0 ? "dollar-sign" : "check";
      break;
    default:
      color = "dark-blue";
      icon += "clock";
  }

  const bgColor = "bg-washed-" + (color === "dark-blue" ? "blue" : color);

  return { icon, color, bgColor };
}

export function getEligibilityAttributes(
  expungement_result: ExpungementResultData,
  caseBalance: number,
  useLongLabel = true
) {
  const { charge_eligibility } = expungement_result;
  let label = charge_eligibility?.label ?? "Unknown";
  const status = charge_eligibility?.status ?? "Unknown";
  const dateStr = charge_eligibility.date_to_sort_label_by;
  const { icon, color, bgColor } = getEligibilityColor(status, caseBalance);

  if (label.match(/\beligible/i) && caseBalance > 0 && useLongLabel) {
    label += " If Balance Paid";
  }

  if (!useLongLabel) {
    if (label === "Needs More Analysis") {
      label = "Needs Analysis";
    }
    if (status === "Will Be Eligible" && dateStr) {
      const date = moment(dateStr, "MMM/D/YY");

      if (date.isValid()) {
        label = "Eligible " + date.format("M/D/YY");
      }
    }
  }

  return { label, color, bgColor, icon };
}

export function newlineOrsInString(
  leading_label: JSX.Element,
  eligibilityString: string
) {
  const splittedElements = eligibilityString.split("OR");

  let boldSpliced = splittedElements.map((element: string, index: number) => {
    return (
      <div
        key={index}
        className={(index > 0 && "bt b--light-gray pt2 mt2") + ""}
      >
        {index === 0 ? leading_label : <span className="fw7">OR </span>}
        {convertCaseNumberIntoLinks(element)}
      </div>
    );
  });
  return boldSpliced;
}

export function convertCaseNumberIntoLinks(eligibilityString: string) {
  const elements = eligibilityString.split(/(\[.*?\])/g);
  return elements.map((element: string, index: number) => {
    if (element.match(/^\[.*\]$/)) {
      const caseNumber = element.slice(1, -1);
      return (
        <a className="underline" href={"#" + caseNumber} key={caseNumber}>
          {caseNumber}
        </a>
      );
    } else {
      return element;
    }
  });
}
