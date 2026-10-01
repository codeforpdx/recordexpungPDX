/**
 * Applies answers to an analysis and recomputes every status.
 *
 * This mirrors `_resolve_outcomes` and `resolve_charge_status` in
 * `expungeservice/models/sb819.py`. The two are executed against the same table in
 * `src/shared/sb819ResolutionFixtures.json` so they cannot drift apart unnoticed.
 */

import {
  SB819AnalysisData,
  SB819Answer,
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819Outcome,
  SB819PathwayResultData,
  SB819Status,
  answerTarget,
} from "./types";

export type SB819Answers = { [target: string]: SB819Answer };

const SEVERITY: { [key in SB819Status]: number } = {
  "Possibly SB-819 Eligible": 0,
  "Needs More Analysis": 1,
  "SB-819 Ineligible": 2,
};

const DISPLAY_ORDER: SB819Status[] = [
  "Possibly SB-819 Eligible",
  "Needs More Analysis",
  "SB-819 Ineligible",
];

function best(statuses: SB819Status[]) {
  return statuses.reduce((a, b) => (SEVERITY[b] < SEVERITY[a] ? b : a));
}

function worst(statuses: SB819Status[]) {
  return statuses.reduce((a, b) => (SEVERITY[b] > SEVERITY[a] ? b : a));
}

/** An answer only ever resolves a criterion that is still open and carries a question. */
export function applyAnswer(
  criterion: SB819CriterionResultData,
  answer: SB819Answer | undefined
): SB819CriterionResultData {
  if (!answer || !criterion.question || criterion.outcome !== "Unknown") {
    return criterion;
  }
  const resulting =
    answer === "yes" ? criterion.question.if_yes : criterion.question.if_no;
  const outcome: SB819Outcome =
    resulting === "SB-819 Ineligible" ? "Failed" : "Passed";
  return { ...criterion, outcome };
}

/**
 * A pathway fails on any failed criterion and is unresolved on any unknown one.
 *
 * Criteria in a disjunction group resolve together: the group passes if any member passes,
 * is unknown if any member is unknown, and fails only if every member fails. Criteria that
 * are not screenable take no part; they are settled by the District Attorney or by
 * documents the applicant assembles later, so nothing here can resolve them.
 */
export function resolveOutcomes(
  criteria: SB819CriterionResultData[]
): SB819Status {
  const screenable = criteria.filter((c) => c.is_screenable);
  const outcomes: SB819Outcome[] = screenable
    .filter((c) => !c.disjunction_group)
    .map((c) => c.outcome);

  const groups = Array.from(
    new Set(
      screenable
        .filter((c) => c.disjunction_group)
        .map((c) => c.disjunction_group)
    )
  );
  groups.forEach((group) => {
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

/**
 * A failed main criterion ends the analysis; no pathway can rescue it. Otherwise the charge
 * is only as good as its best pathway, and never better than its main criteria.
 */
export function resolveChargeStatus(
  mainStatus: SB819Status,
  pathwayStatuses: SB819Status[]
): SB819Status {
  if (mainStatus === "SB-819 Ineligible") return "SB-819 Ineligible";
  if (pathwayStatuses.length === 0) return mainStatus;
  return worst([mainStatus, best(pathwayStatuses)]);
}

function resolveCharge(
  charge: SB819ChargeAnalysisData,
  answers: SB819Answers
): SB819ChargeAnalysisData {
  const answerFor = (criterion: SB819CriterionResultData) =>
    answers[
      answerTarget(criterion, charge.case_number, charge.ambiguous_charge_id)
    ];

  const main = charge.main_criteria.map((c) => applyAnswer(c, answerFor(c)));
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

  const pathways: SB819PathwayResultData[] = charge.pathways.map((pathway) => {
    const criteria = pathway.criteria.map((c) => applyAnswer(c, answerFor(c)));
    return { ...pathway, criteria, status: resolveOutcomes(criteria) };
  });

  return {
    ...charge,
    main_criteria: main,
    pathways,
    status: resolveChargeStatus(
      mainStatus,
      pathways.map((p) => p.status)
    ),
    available_pathways: pathways
      .filter((p) => p.status !== "SB-819 Ineligible")
      .map((p) => p.pathway),
    blocked_pathways: pathways
      .filter((p) => p.status === "SB-819 Ineligible")
      .map((p) => p.pathway),
  };
}

export default function resolveAnalysis(
  analysis: SB819AnalysisData,
  answers: SB819Answers
): SB819AnalysisData {
  const charges: SB819AnalysisData["charges"] = {};
  Object.entries(analysis.charges).forEach(([id, charge]) => {
    charges[id] = resolveCharge(charge, answers);
  });

  const resolved = Object.values(charges);

  return {
    ...analysis,
    charges,
    has_possibly_eligible: resolved.some(
      (c) => c.status !== "SB-819 Ineligible"
    ),
    sections: DISPLAY_ORDER.map((status) => ({
      status,
      charge_ids: resolved
        .filter((c) => c.status === status)
        .map((c) => c.ambiguous_charge_id),
    })),
  };
}

/**
 * The failed criteria that bar a pathway, in the order they were evaluated.
 *
 * A criterion in a disjunction group only disqualifies when every alternative in that group
 * failed. One failed alternative among several is not a bar, and naming it as one would
 * report a disqualification the criteria do not impose.
 *
 * Mirrors `disqualifying_results` in expungeservice/models/sb819.py.
 */
export function disqualifyingCriteria(
  criteria: SB819CriterionResultData[]
): SB819CriterionResultData[] {
  const screenable = criteria.filter((c) => c.is_screenable);
  const fullyFailedGroups = new Set(
    Array.from(
      new Set(screenable.map((c) => c.disjunction_group).filter(Boolean))
    ).filter((group) =>
      screenable
        .filter((c) => c.disjunction_group === group)
        .every((c) => c.outcome === "Failed")
    )
  );
  return screenable.filter(
    (c) =>
      c.outcome === "Failed" &&
      (!c.disjunction_group || fullyFailedGroups.has(c.disjunction_group))
  );
}
