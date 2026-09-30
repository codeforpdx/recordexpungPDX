/**
 * Resolution: the analysis plus the answers, to a status for every pathway and charge.
 *
 * The same algebra runs in Python when the record is analyzed and here when a volunteer
 * answers a question. Both are executed against src/shared/sb819ResolutionFixtures.json,
 * so they cannot drift apart unnoticed.
 */

import {
  AnalysisData,
  Answer,
  Answers,
  ChargeAnalysisData,
  CriterionData,
  Outcome,
  PathwayData,
  STATUSES,
  Status,
  targetOf,
} from "./types";

const SEVERITY: { [key in Status]: number } = {
  "Possibly SB-819 Eligible": 0,
  "Needs More Analysis": 1,
  "SB-819 Ineligible": 2,
};

const best = (statuses: Status[]) =>
  statuses.reduce((a, b) => (SEVERITY[b] < SEVERITY[a] ? b : a));

const worst = (statuses: Status[]) =>
  statuses.reduce((a, b) => (SEVERITY[b] > SEVERITY[a] ? b : a));

/**
 * An answer resolves a criterion the record left unknown and the client can settle. A
 * resulting status of Ineligible is a failure; anything else is a pass. Any other criterion
 * is returned untouched.
 */
export function applyAnswer(
  criterion: CriterionData,
  answer: Answer | undefined
): CriterionData {
  if (!answer || !criterion.question || criterion.outcome !== "Unknown") {
    return criterion;
  }
  const status =
    answer === "yes" ? criterion.question.if_yes : criterion.question.if_no;
  const outcome: Outcome = status === "SB-819 Ineligible" ? "Failed" : "Passed";
  return { ...criterion, outcome };
}

const groupsOf = (criteria: CriterionData[]) =>
  Array.from(new Set(criteria.map((c) => c.disjunction_group).filter(Boolean)));

/**
 * Over the screenable criteria: any failure gives Ineligible, else any unknown gives Needs
 * More Analysis, else Possibly Eligible. A disjunction group counts once: passed if any
 * member passed, unknown if any member is unknown, failed only when every member failed.
 */
export function resolveOutcomes(criteria: CriterionData[]): Status {
  const screenable = criteria.filter((c) => c.is_screenable);
  const outcomes: Outcome[] = screenable
    .filter((c) => !c.disjunction_group)
    .map((c) => c.outcome);

  groupsOf(screenable).forEach((group) => {
    const members = screenable
      .filter((c) => c.disjunction_group === group)
      .map((c) => c.outcome);
    if (members.includes("Passed")) outcomes.push("Passed");
    else if (members.includes("Unknown")) outcomes.push("Unknown");
    else outcomes.push("Failed");
  });

  if (outcomes.includes("Failed")) return "SB-819 Ineligible";
  if (outcomes.includes("Unknown")) return "Needs More Analysis";
  return "Possibly SB-819 Eligible";
}

/** A failed main criterion ends the analysis. Otherwise the charge is the worse of its main
 * status and its best pathway status. */
export function resolveChargeStatus(
  mainStatus: Status,
  pathwayStatuses: Status[]
): Status {
  if (mainStatus === "SB-819 Ineligible") return "SB-819 Ineligible";
  if (pathwayStatuses.length === 0) return mainStatus;
  return worst([mainStatus, best(pathwayStatuses)]);
}

/**
 * The failed criteria that bar a pathway, in evaluation order: those not in a group, and
 * the members of any group whose every member failed. One failed alternative among
 * several is not a bar.
 */
export function disqualifyingCriteria(
  criteria: CriterionData[]
): CriterionData[] {
  const screenable = criteria.filter((c) => c.is_screenable);
  const failedGroups = new Set(
    groupsOf(screenable).filter((group) =>
      screenable
        .filter((c) => c.disjunction_group === group)
        .every((c) => c.outcome === "Failed")
    )
  );
  return screenable.filter(
    (c) =>
      c.outcome === "Failed" &&
      (!c.disjunction_group || failedGroups.has(c.disjunction_group))
  );
}

function resolveCharge(
  charge: ChargeAnalysisData,
  answers: Answers
): ChargeAnalysisData {
  const apply = (c: CriterionData) =>
    applyAnswer(c, answers[targetOf(c, charge)]);

  const main = charge.main_criteria.map(apply);
  const mainStatus = resolveOutcomes(main);
  if (mainStatus === "SB-819 Ineligible") {
    return {
      ...charge,
      main_criteria: main,
      pathways: [],
      status: "SB-819 Ineligible",
      available_pathways: [],
      blocked_pathways: [],
    };
  }

  const pathways: PathwayData[] = charge.pathways.map((pathway) => {
    const criteria = pathway.criteria.map(apply);
    return { ...pathway, criteria, status: resolveOutcomes(criteria) };
  });
  const blocked = pathways.filter((p) => p.status === "SB-819 Ineligible");
  const open = pathways.filter((p) => p.status !== "SB-819 Ineligible");

  return {
    ...charge,
    main_criteria: main,
    pathways,
    status: resolveChargeStatus(
      mainStatus,
      pathways.map((p) => p.status)
    ),
    available_pathways: open.map((p) => p.pathway),
    blocked_pathways: blocked.map((p) => p.pathway),
  };
}

/** The whole analysis with every answer applied and every status and section recomputed. */
export default function resolveAnalysis(
  analysis: AnalysisData,
  answers: Answers
): AnalysisData {
  const charges: AnalysisData["charges"] = {};
  Object.entries(analysis.charges).forEach(([id, charge]) => {
    charges[id] = resolveCharge(charge, answers);
  });
  const all = Object.values(charges);
  return {
    ...analysis,
    charges,
    has_possibly_eligible: all.some((c) => c.status !== "SB-819 Ineligible"),
    sections: STATUSES.map((status) => ({
      status,
      charge_ids: all
        .filter((c) => c.status === status)
        .map((c) => c.ambiguous_charge_id),
    })),
  };
}
