/**
 * The SB-819 analysis as the search payload carries it, and the answers laid over it.
 *
 * Mirrors `sb819_analysis_to_json` in expungeservice/serializer.py. The view never
 * rewrites a string the payload supplies.
 */

export const STATUSES = [
  "Possibly SB-819 Eligible",
  "Needs More Analysis",
  "SB-819 Ineligible",
] as const;

export type Status = (typeof STATUSES)[number];

export type Pathway =
  | "Actual Innocence"
  | "Excessive Sentencing"
  | "Collateral Consequences";

/** OECI: the record settles it. Question: the client does. The other two are settled
 * later, by the District Attorney or by documents, and take no part in any status. */
export type Determination = "OECI" | "Question" | "Discretion" | "Part 2";

export type Outcome = "Passed" | "Failed" | "Unknown";

export type Scope = "record" | "case" | "charge";

export type Answer = "yes" | "no";

export interface QuestionData {
  text: string;
  if_yes: Status;
  if_no: Status;
  note: string;
}

export interface CriterionData {
  key: string;
  scope: Scope;
  disjunction_group: string;
  is_gate: boolean;
  is_screenable: boolean;
  name: string;
  description: string;
  citation: string;
  determination: Determination;
  pathway: Pathway | null;
  outcome: Outcome;
  explanation: string;
  question: QuestionData | null;
}

export interface PathwayData {
  pathway: Pathway;
  status: Status;
  criteria: CriterionData[];
}

export interface ChargeAnalysisData {
  ambiguous_charge_id: string;
  case_number: string;
  charge_name: string;
  status: Status;
  main_criteria: CriterionData[];
  pathways: PathwayData[];
  available_pathways: Pathway[];
  blocked_pathways: Pathway[];
}

export interface SectionData {
  status: Status;
  charge_ids: string[];
}

export interface AnalysisData {
  counties_analyzed: string[];
  has_analyzed_charges: boolean;
  has_possibly_eligible: boolean;
  sections: SectionData[];
  charges: { [ambiguous_charge_id: string]: ChargeAnalysisData };
}

/** Answers keyed by target; see `targetOf`. */
export type Answers = { [target: string]: Answer | undefined };

/**
 * Where a question's answer is stored, so one answer reaches every charge it governs: a
 * record-scope answer reaches every charge, a case-scope answer every charge on its case.
 */
export function targetOf(criterion: CriterionData, charge: ChargeAnalysisData) {
  switch (criterion.scope) {
    case "record":
      return `record:${criterion.key}`;
    case "case":
      return `case:${charge.case_number}:${criterion.key}`;
    default:
      return `charge:${charge.ambiguous_charge_id}:${criterion.key}`;
  }
}

/** A criterion the client can settle: screenable, and the record left it a question. */
export function isQuestion(criterion: CriterionData) {
  return criterion.is_screenable && criterion.question !== null;
}

export function statusColor(status: Status) {
  return {
    "Possibly SB-819 Eligible": "green",
    "Needs More Analysis": "purple",
    "SB-819 Ineligible": "red",
  }[status];
}
