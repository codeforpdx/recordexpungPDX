import React from "react";
import { DateTime } from "luxon";
import { ExpungementResultData, ChargeEligibilityStatus } from "./types";

type EligibilityColor = "green" | "dark-blue" | "purple" | "red";

export function getEligibilityColor(status: string, caseBalance = 0) {
  let color: EligibilityColor;
  let icon = "fa fa-";

  switch (status) {
    case "Eligible":
    case "Eligible Future":
      color = "dark-blue";
      icon = "dollar-sign";
      break;
    case "Eligible Now":
      color = caseBalance > 0 ? "dark-blue" : "green";
      icon += caseBalance > 0 ? "dollar-sign" : "check";
      break;
    case "Ineligible":
      color = "red";
      icon += "circle-xmark";
      break;
    case "Will Be Eligible":
      color = "dark-blue";
      icon += "clock";
      break;
    case "Possibly Eligible":
    case "Possibly Will Be Eligible":
    case "Unknown":
    case "Needs More Analysis":
    default:
      color = "purple";
      icon += "question-circle";
  }

  const bgColor = "bg-washed-" + (color === "dark-blue" ? "blue" : color);

  return { icon, color, bgColor };
}

export function getShortLabel(
  status: ChargeEligibilityStatus,
  dateStr?: string | null,
  caseBalance?: number
) {
  const date = dateStr && DateTime.fromFormat(dateStr, "MMM d, yyyy");

  switch (status) {
    case "Eligible Now":
      if (caseBalance && caseBalance > 0) return "Eligible";
      return status;
    case "Will Be Eligible":
      if (!date || !date.isValid) return "Eligible Future";
      return "Eligible " + date.toFormat("M/d/yy");
    case "Needs More Analysis":
      return "Needs Analysis";
    case "Possibly Eligible":
    case "Possibly Will Be Eligible":
      return "Eligible?";
    case "Ineligible":
    case "Unknown":
    default:
      return status;
  }
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

  if (label.match(/\beligible/i) && caseBalance > 0 && useLongLabel) {
    label += " If Balance Paid";
  }

  if (!useLongLabel) {
    label = getShortLabel(status, dateStr, caseBalance);
  }

  return { label, ...getEligibilityColor(status, caseBalance) };
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
