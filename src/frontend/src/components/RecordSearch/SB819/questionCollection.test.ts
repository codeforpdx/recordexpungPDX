import resolveAnalysis, { SB819Answers } from "./resolveAnalysis";
import {
  awaiting,
  chargeIdsForCase,
  questionsAt,
  shown,
  stateOf,
} from "./questionCollection";
import { buildAnalysis } from "./sb819TestData";
import { SB819AnalysisData } from "./types";

const resolved = (analysis: SB819AnalysisData, answers: SB819Answers) =>
  resolveAnalysis(analysis, answers);

function states(
  analysis: SB819AnalysisData,
  scope: "case" | "charge",
  answers: SB819Answers,
  chargeIds?: string[]
) {
  const a = resolved(analysis, answers);
  return Object.fromEntries(
    questionsAt(a, scope, chargeIds).map((q) => [
      q.criterion.key,
      stateOf(q, answers),
    ])
  );
}

describe("a case's questions", () => {
  it("opens with the pathway's gate, sentence completion", () => {
    const analysis = buildAnalysis();
    const ids = chargeIdsForCase(analysis, "100");
    expect(states(analysis, "case", {}, ids)).toEqual({
      "sentence-completed": "live",
    });
  });

  it("is carried by every conviction on the case and collected once", () => {
    const analysis = resolved(buildAnalysis({ theft: true }), {});
    const questions = questionsAt(
      analysis,
      "case",
      chargeIdsForCase(analysis, "100")
    );
    expect(questions.map((q) => q.target)).toEqual([
      "case:100:sentence-completed",
    ]);
    expect(
      questions[0].carriers.map((c) => c.charge.ambiguous_charge_id)
    ).toEqual(["100-1", "100-2"]);
  });

  it("has nothing to ask on a charge the record rules out", () => {
    const analysis = buildAnalysis({ duii: true, rape: true });
    expect(questionsAt(resolved(analysis, {}), "case", ["300-1"])).toEqual([]);
    // Collateral Consequences is ruled out by the registerable offense, so its gate is moot here.
    expect(states(analysis, "case", {}, ["500-1"])["sentence-completed"]).toBe(
      "dormant"
    );
  });

  it("waits on an open felony question when that is the only charge", () => {
    const analysis = buildAnalysis({ assault: true });
    const only = ["800-1"];
    expect(states(analysis, "case", {}, only)).toEqual({
      "sentence-completed": "dormant",
    });
    expect(states(analysis, "charge", {}, only)).toEqual({
      "sentenced-as-felony": "live",
      "no-domestic-violence": "dormant",
    });
  });
});

describe("a charge's questions", () => {
  it("hold behind the case's gate", () => {
    expect(states(buildAnalysis(), "charge", {}, ["100-1"])).toEqual({
      "no-domestic-violence": "dormant",
    });
  });

  it("are put once the gate is met", () => {
    const answers: SB819Answers = { "case:100:sentence-completed": "yes" };
    expect(states(buildAnalysis(), "charge", answers, ["100-1"])).toEqual({
      "no-domestic-violence": "live",
    });
  });

  it("stand down once the pathway is ruled out by the gate", () => {
    const answers: SB819Answers = { "case:100:sentence-completed": "no" };
    expect(
      states(buildAnalysis(), "charge", answers, ["100-1"])[
        "no-domestic-violence"
      ]
    ).toBe("dormant");
  });

  it("keep an answered question on screen after the gate turns against it", () => {
    const answers: SB819Answers = {
      "case:100:sentence-completed": "no",
      "charge:100-1:no-domestic-violence": "no",
    };
    expect(states(buildAnalysis(), "charge", answers, ["100-1"])).toEqual({
      "no-domestic-violence": "answered",
    });
  });

  it("leave only the felony question once it is answered against", () => {
    // A failed main criterion empties the pathways, and their questions with them.
    const answers: SB819Answers = {
      "charge:800-1:sentenced-as-felony": "no",
      "case:800:sentence-completed": "yes",
    };
    expect(
      states(buildAnalysis({ assault: true }), "charge", answers, ["800-1"])
    ).toEqual({ "sentenced-as-felony": "answered" });
  });
});

describe("the stage predicates", () => {
  it("wait on live questions only", () => {
    const analysis = resolved(buildAnalysis(), {});
    const caseQuestions = questionsAt(analysis, "case");
    expect(awaiting(caseQuestions, {})).toBe(true);
    expect(shown(caseQuestions, {}).map((q) => q.criterion.key)).toEqual([
      "sentence-completed",
    ]);
    const answers: SB819Answers = { "case:100:sentence-completed": "no" };
    expect(
      awaiting(questionsAt(resolved(buildAnalysis(), answers), "case"), answers)
    ).toBe(false);
  });
});
