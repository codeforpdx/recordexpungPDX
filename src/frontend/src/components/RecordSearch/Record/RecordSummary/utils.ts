import { DateTime } from "luxon";

export function getEligibilityColor(eligibility: string) {
  return (
    {
      "Eligible Now": "green",
      Ineligible: "red",
      "Eligible on case with Ineligible charge": "red",
      "Needs More Analysis": "purple",
    }[eligibility] ?? "dark-blue"
  );
}

export function getFinalEligibility(
  status: string,
  dateEligible: string,
  caseBalance: number
) {
  let finalStatus = status;

  if (dateEligible) {
    const eligibleDate = DateTime.fromFormat(dateEligible, "MMM d, yyyy");
    const isEligibleNow = DateTime.now() >= eligibleDate;

    if (finalStatus === "Eligible") {
      if (isEligibleNow) {
        finalStatus += caseBalance > 0 ? " Now If Balance Paid" : " Now";
      } else {
        finalStatus += " " + dateEligible;
      }
    }
  }

  return finalStatus;
}
