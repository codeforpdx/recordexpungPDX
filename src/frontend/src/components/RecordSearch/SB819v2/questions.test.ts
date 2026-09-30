import resolveAnalysis from "./resolve";
import {
  awaiting,
  chargeIdsOnCase,
  questionsAt,
  shown,
  stateOf,
} from "./questions";
import { buildAnalysis } from "./testData";
import { AnalysisData, Answers } from "./types";

const resolved = (analysis: AnalysisData, answers: Answers) =>
  resolveAnalysis(analysis, answers);

function states(
  analysis: AnalysisData,
  scope: "record" | "case" | "charge",
  answers: Answers,
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

describe("the applicant's questions", () => {
  it("opens with the gate alone; the alternatives wait on it", () => {
    expect(states(buildAnalysis(), "record", {})).toEqual({
      "currently-incarcerated": "live",
      "juvenile-transfer": "dormant",
      "over-60-or-ill": "dormant",
      "person-over-16-years": "dormant",
    });
  });

  it("puts the alternatives once the gate is met, and only those the record leaves open", () => {
    // Robbery II is a person crime, so the non-person alternative failed from the record.
    const answers: Answers = { "record:currently-incarcerated": "yes" };
    expect(states(buildAnalysis(), "record", answers)).toEqual({
      "currently-incarcerated": "answered",
      "juvenile-transfer": "live",
      "over-60-or-ill": "live",
      "person-over-16-years": "live",
    });
  });

  it("asks the non-person alternative when some charge is a non-person crime", () => {
    const answers: Answers = { "record:currently-incarcerated": "yes" };
    expect(
      states(buildAnalysis({ theft: true }), "record", answers)[
        "non-person-over-10-years"
      ]
    ).toBe("live");
  });

  it("stands the other alternatives down once one is met", () => {
    const answers: Answers = {
      "record:currently-incarcerated": "yes",
      "record:juvenile-transfer": "yes",
    };
    expect(states(buildAnalysis(), "record", answers)).toEqual({
      "currently-incarcerated": "answered",
      "juvenile-transfer": "answered",
      "over-60-or-ill": "dormant",
      "person-over-16-years": "dormant",
    });
  });

  it("keeps an answered alternative on screen after the gate turns against it", () => {
    const answers: Answers = {
      "record:currently-incarcerated": "no",
      "record:over-60-or-ill": "yes",
    };
    expect(states(buildAnalysis(), "record", answers)).toEqual({
      "currently-incarcerated": "answered",
      "juvenile-transfer": "dormant",
      "over-60-or-ill": "answered",
      "person-over-16-years": "dormant",
    });
  });

  it("does not stand the alternatives down while a met alternative is on another charge only", () => {
    // Arson I was committed under 18, which meets the group on that charge alone.
    const answers: Answers = { "record:currently-incarcerated": "yes" };
    expect(
      states(buildAnalysis({ arson: true }), "record", answers)[
        "over-60-or-ill"
      ]
    ).toBe("live");
  });

  it("holds every question behind an open felony question when that is the only charge", () => {
    const analysis = buildAnalysis({ assault: true });
    const only = ["800-1"];
    expect(states(analysis, "record", {}, only)).toEqual({
      "currently-incarcerated": "dormant",
      "juvenile-transfer": "dormant",
      "over-60-or-ill": "dormant",
      "person-over-16-years": "dormant",
    });
    expect(states(analysis, "case", {}, only)).toEqual({
      "not-global-plea": "dormant",
      "sentence-completed": "dormant",
    });
    expect(states(analysis, "charge", {}, only)).toEqual({
      "sentenced-as-felony": "live",
      "innocence-claim": "dormant",
      "five-years-served": "dormant",
      "no-domestic-violence": "dormant",
    });
  });
});

describe("a case's questions", () => {
  it("opens with sentence completion; the plea question waits on the applicant's gate", () => {
    const analysis = buildAnalysis();
    const ids = chargeIdsOnCase(analysis, "100");
    expect(states(analysis, "case", {}, ids)).toEqual({
      "not-global-plea": "dormant",
      "sentence-completed": "live",
    });
    expect(
      states(analysis, "case", { "record:currently-incarcerated": "yes" }, ids)[
        "not-global-plea"
      ]
    ).toBe("live");
  });

  it("has nothing to ask on a charge the record rules out", () => {
    const analysis = buildAnalysis({ duii: true, rape: true });
    expect(questionsAt(resolved(analysis, {}), "case", ["300-1"])).toEqual([]);
    // Collateral Consequences is ruled out by the registerable offense, so its gate is moot here.
    expect(states(analysis, "case", {}, ["500-1"])["sentence-completed"]).toBe(
      "dormant"
    );
  });
});

describe("a charge's questions", () => {
  it("shows the innocence claim at once and the rest behind their gates", () => {
    expect(states(buildAnalysis(), "charge", {}, ["100-1"])).toEqual({
      "innocence-claim": "live",
      "five-years-served": "dormant",
      "no-domestic-violence": "dormant",
    });
  });

  it("puts the gated questions once each gate is met", () => {
    const answers: Answers = {
      "record:currently-incarcerated": "yes",
      "case:100:sentence-completed": "yes",
    };
    expect(states(buildAnalysis(), "charge", answers, ["100-1"])).toEqual({
      "innocence-claim": "live",
      "five-years-served": "live",
      "no-domestic-violence": "live",
    });
  });

  it("stands a question down once its pathway is ruled out by another answer", () => {
    const answers: Answers = {
      "record:currently-incarcerated": "yes",
      "case:100:not-global-plea": "yes",
    };
    expect(
      states(buildAnalysis(), "charge", answers, ["100-1"])["five-years-served"]
    ).toBe("dormant");
  });

  it("leaves only the felony question once it is answered against", () => {
    // A failed main criterion empties the pathways, and their questions with them.
    const answers: Answers = {
      "charge:800-1:sentenced-as-felony": "no",
      "record:currently-incarcerated": "yes",
    };
    expect(
      states(buildAnalysis({ assault: true }), "charge", answers, ["800-1"])
    ).toEqual({ "sentenced-as-felony": "answered" });
  });
});

describe("the stage predicates", () => {
  it("wait on live questions only", () => {
    const analysis = resolved(buildAnalysis(), {});
    const applicant = questionsAt(analysis, "record");
    expect(awaiting(applicant, {})).toBe(true);
    expect(shown(applicant, {}).map((q) => q.criterion.key)).toEqual([
      "currently-incarcerated",
    ]);
    expect(
      awaiting(
        questionsAt(
          resolved(buildAnalysis(), { "record:currently-incarcerated": "no" }),
          "record"
        ),
        { "record:currently-incarcerated": "no" }
      )
    ).toBe(false);
  });
});
