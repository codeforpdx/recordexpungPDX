/**
 * The frontend half of the shared resolution table, src/shared/sb819ResolutionFixtures.json,
 * which the backend executes too. Each scenario is run through the whole resolver as a
 * one-charge analysis, so the top-level function is under test and not only its parts.
 */

import fs from "fs";
import path from "path";
import resolveAnalysis, {
  SB819Answers,
  disqualifyingCriteria,
} from "./resolveAnalysis";
import {
  SB819AnalysisData,
  SB819CriterionResultData,
  SB819Determination,
  SB819Outcome,
  SB819Status,
} from "./types";

const FIXTURES = path.resolve(
  __dirname,
  "../../../../../shared/sb819ResolutionFixtures.json"
);

interface FixtureCriterion {
  key: string;
  determination: SB819Determination;
  outcome: SB819Outcome;
  group?: string;
  question?: { if_yes: SB819Status; if_no: SB819Status };
}

interface Scenario {
  name: string;
  main: FixtureCriterion[];
  pathways: { pathway: string; criteria: FixtureCriterion[] }[];
  answers?: { [key: string]: "yes" | "no" };
  expect: {
    charge: SB819Status;
    pathways?: { [pathway: string]: SB819Status };
    pathways_not_evaluated?: boolean;
    disqualifying?: string[];
  };
}

const CHARGE = "c1";

function build(entry: FixtureCriterion): SB819CriterionResultData {
  return {
    key: entry.key,
    scope: "charge",
    disjunction_group: entry.group ?? "",
    is_gate: false,
    is_screenable:
      entry.determination === "OECI" || entry.determination === "Question",
    name: entry.key,
    description: "",
    citation: "",
    determination: entry.determination,
    pathway: null,
    outcome: entry.outcome,
    explanation: "",
    question: entry.question
      ? { text: entry.key, note: "", ...entry.question }
      : null,
  };
}

function analysisFor(scenario: Scenario): SB819AnalysisData {
  return {
    counties_analyzed: ["Multnomah"],
    has_analyzed_charges: true,
    has_possibly_eligible: true,
    sections: [],
    charges: {
      [CHARGE]: {
        ambiguous_charge_id: CHARGE,
        case_number: "1",
        charge_name: scenario.name,
        status: "Needs More Analysis",
        main_criteria: scenario.main.map(build),
        pathways: scenario.pathways.map((p) => ({
          pathway: p.pathway as any,
          status: "Needs More Analysis",
          criteria: p.criteria.map(build),
        })),
        available_pathways: [],
        blocked_pathways: [],
      },
    },
  };
}

function runScenario(scenario: Scenario) {
  const answers: SB819Answers = {};
  Object.entries(scenario.answers ?? {}).forEach(([key, answer]) => {
    answers[`charge:${CHARGE}:${key}`] = answer;
  });
  const charge = resolveAnalysis(analysisFor(scenario), answers).charges[
    CHARGE
  ];

  expect(charge.status).toBe(scenario.expect.charge);
  if (scenario.expect.pathways_not_evaluated) {
    expect(charge.pathways).toEqual([]);
    return;
  }
  charge.pathways.forEach((pathway) => {
    expect([pathway.pathway, pathway.status]).toEqual([
      pathway.pathway,
      scenario.expect.pathways![pathway.pathway],
    ]);
  });
  if (scenario.expect.disqualifying) {
    const barred = charge.pathways.flatMap((p) =>
      disqualifyingCriteria(p.criteria).map((c) => c.key)
    );
    expect(barred).toEqual(scenario.expect.disqualifying);
  }
}

const table = JSON.parse(fs.readFileSync(FIXTURES, "utf8"));

describe("outcome scenarios, shared with the backend", () => {
  (table.outcome_scenarios as Scenario[]).forEach((scenario) => {
    it(scenario.name, () => runScenario(scenario));
  });
});

describe("answer scenarios", () => {
  (table.answer_scenarios as Scenario[]).forEach((scenario) => {
    it(scenario.name, () => runScenario(scenario));
  });
});

it("re-buckets the sections and the badge flag on every answer", () => {
  const scenario = (table.answer_scenarios as Scenario[]).find((s) =>
    s.name.startsWith("a disqualifying answer")
  )!;
  const answers: SB819Answers = {};
  Object.entries(scenario.answers!).forEach(([key, answer]) => {
    answers[`charge:${CHARGE}:${key}`] = answer;
  });
  const resolved = resolveAnalysis(analysisFor(scenario), answers);
  expect(resolved.sections.map((s) => [s.status, s.charge_ids])).toEqual([
    ["Possibly SB-819 Eligible", []],
    ["Needs More Analysis", []],
    ["SB-819 Ineligible", [CHARGE]],
  ]);
  expect(resolved.has_possibly_eligible).toBe(false);
});
