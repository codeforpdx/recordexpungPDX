export const sb819Statuses = [
  "Possibly SB-819 Eligible",
  "Needs More Analysis",
  "SB-819 Ineligible",
] as const;

export type SB819Status = (typeof sb819Statuses)[number];

export type SB819Pathway = "Collateral Consequences";

/** How a criterion is settled. OECI reads the record and Question asks the client. Part 2
 * is settled by documents the applicant assembles later, so it takes no part in any status
 * and is shown as an instruction. */
export type SB819Determination = "OECI" | "Question" | "Part 2";

export type SB819Outcome = "Passed" | "Failed" | "Unknown";

export interface SB819QuestionData {
  text: string;
  if_yes: SB819Status;
  if_no: SB819Status;
  note: string;
}

export type SB819Scope = "case" | "charge";

export type SB819Answer = "yes" | "no";

export interface SB819CriterionResultData {
  key: string;
  scope: SB819Scope;
  /** The question that defines who the pathway is for; its other questions wait on this one. */
  is_gate: boolean;
  is_screenable: boolean;
  name: string;
  description: string;
  citation: string;
  determination: SB819Determination;
  pathway: SB819Pathway | null;
  outcome: SB819Outcome;
  explanation: string;
  question: SB819QuestionData | null;
}

export interface SB819PathwayResultData {
  pathway: SB819Pathway;
  status: SB819Status;
  criteria: SB819CriterionResultData[];
}

export interface SB819ChargeAnalysisData {
  ambiguous_charge_id: string;
  case_number: string;
  charge_name: string;
  status: SB819Status;
  main_criteria: SB819CriterionResultData[];
  pathways: SB819PathwayResultData[];
}

export interface SB819SectionData {
  status: SB819Status;
  charge_ids: string[];
}

export interface SB819AnalysisData {
  counties_analyzed: string[];
  has_analyzed_charges: boolean;
  has_possibly_eligible: boolean;
  sections: SB819SectionData[];
  charges: { [ambiguous_charge_id: string]: SB819ChargeAnalysisData };
}

/** Where a criterion's answer is held, so one answer reaches every charge it governs. */
export function answerTarget(
  criterion: SB819CriterionResultData,
  caseNumber: string,
  ambiguousChargeId: string
): string {
  return criterion.scope === "case"
    ? `case:${caseNumber}:${criterion.key}`
    : `charge:${ambiguousChargeId}:${criterion.key}`;
}

/**
 * Why a criterion barred a pathway, phrased as what happened rather than what was required.
 *
 * Criterion names are requirements, some positive ("Applicant is currently incarcerated")
 * and some negative ("Conviction is not aggravated murder"), so a name shown as a reason
 * states the opposite of the failure. A criterion settled from the record carries an
 * explanation written for exactly this. One settled by the client is reported as the
 * question and the answer given, which is the only honest account of it.
 */
export function failureReason(criterion: SB819CriterionResultData): {
  text: string;
  answer?: "Yes" | "No";
} {
  if (criterion.question) {
    // Only an answer can fail a criterion that still carries a question, and the failing
    // answer is whichever branch leads to ineligibility.
    const answer =
      criterion.question.if_yes === "SB-819 Ineligible" ? "Yes" : "No";
    return { text: criterion.question.text, answer };
  }
  return { text: criterion.explanation };
}

export function statusColor(status: SB819Status) {
  return (
    {
      "Possibly SB-819 Eligible": "green",
      "Needs More Analysis": "purple",
      "SB-819 Ineligible": "red",
    }[status] ?? "dark-blue"
  );
}

export function statusBackground(status: SB819Status) {
  return "bg-washed-" + statusColor(status);
}

export function outcomeIcon(outcome: SB819Outcome) {
  return (
    {
      Passed: "fas fa-check-circle green",
      Failed: "fas fa-times-circle red",
      Unknown: "fas fa-question-circle purple",
    }[outcome] ?? "fas fa-question-circle purple"
  );
}
