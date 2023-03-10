import moment from "moment";

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
    const eligibleDate = moment(dateEligible, "MMM D, YYYY");
    const isEligibleNow = moment().isSameOrAfter(eligibleDate);

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
