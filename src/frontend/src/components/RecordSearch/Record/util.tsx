import React from "react";
import { DateTime } from "luxon";
import {
  ExpungementResultData,
  ChargeEligibilityStatus,
  SetAsideMotionData,
  SetAsideMotionEdit,
} from "./types";

type EligibilityColor = "green" | "dark-blue" | "purple" | "red" | "blue";

/** The API's "MMM d, yyyy" date as the editor's "M/d/yyyy"; an empty or unparseable date stays as given. */
export function shortToMMDDYYYY(shortDate: string | null | undefined) {
  if (!shortDate) return "";
  const date = DateTime.fromFormat(shortDate, "MMM d, yyyy");
  return date.isValid ? date.toFormat("M/d/yyyy") : shortDate;
}

/** The case's motion in the form the editor sends, so an unrelated case edit carries it unchanged. */
export function motionEditFrom(
  motion: SetAsideMotionData | null | undefined
): SetAsideMotionEdit {
  if (!motion) return { status: "None", filed_date: "", resolved_date: "" };
  return {
    status: motion.status,
    filed_date: shortToMMDDYYYY(motion.filed_date),
    resolved_date: shortToMMDDYYYY(motion.resolved_date),
  };
}

/** The sentence shown for a case's motion: open, or closed with how and when. */
export function describeMotion(motion: SetAsideMotionData) {
  const filed = `A motion to set aside this case was filed on ${motion.filed_date}`;
  if (motion.status === "Filed") return `${filed}.`;
  const verb = motion.status === "Denied" ? "denied" : "withdrawn";
  const when = motion.resolved_date ? ` on ${motion.resolved_date}` : "";
  return `${filed} and ${verb}${when}.`;
}

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
    case "Motion Previously Filed":
      color = "blue";
      icon += "gavel";
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
    case "Motion Previously Filed":
      return "Motion Filed";
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
