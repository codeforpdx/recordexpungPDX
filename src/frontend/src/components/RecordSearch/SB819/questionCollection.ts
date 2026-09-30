/**
 * Question state: which questions are answered, which are live, and which are dormant.
 *
 * Every function here reads the resolved analysis (see resolve.ts), so "unknown" on a
 * criterion means the record left it open and no answer has settled it.
 */

import { SB819Answers } from "./resolveAnalysis";
import {
  SB819AnalysisData,
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819Scope,
  answerTarget,
} from "./types";

/** A criterion the client can settle: screenable, and the record left it a question. */
export function isQuestion(criterion: SB819CriterionResultData) {
  return criterion.is_screenable && criterion.question !== null;
}

export interface Question {
  /** The criterion as the first charge that carries it reports it. */
  criterion: SB819CriterionResultData;
  target: string;
  /** Every charge that puts this question, with that charge's own copy of the criterion. */
  carriers: {
    charge: SB819ChargeAnalysisData;
    criterion: SB819CriterionResultData;
  }[];
}

export type QuestionState = "answered" | "live" | "dormant";

const mainFailed = (charge: SB819ChargeAnalysisData) =>
  charge.main_criteria.some((c) => c.is_screenable && c.outcome === "Failed");

const openMainQuestion = (charge: SB819ChargeAnalysisData) =>
  charge.main_criteria.some((c) => isQuestion(c) && c.outcome === "Unknown");

/**
 * Whether answering this criterion's question now could change a status on this charge.
 *
 * It cannot when the record or an answer has already settled it; when the charge is out on
 * its main criteria; when the pathway is already ruled out; while a main-criterion question
 * on the charge is open, since a conviction not sentenced as a felony is out under every
 * pathway; while the pathway's gate has not passed, since the gate says who the pathway is
 * for; or once another alternative in its group has passed, since one met alternative
 * satisfies the group.
 */
export function liveOnCharge(
  charge: SB819ChargeAnalysisData,
  criterion: SB819CriterionResultData
): boolean {
  if (!isQuestion(criterion) || criterion.outcome !== "Unknown") return false;
  if (mainFailed(charge)) return false;
  if (criterion.pathway === null) return true;

  if (openMainQuestion(charge)) return false;
  const pathway = charge.pathways.find((p) => p.pathway === criterion.pathway);
  if (!pathway || pathway.status === "SB-819 Ineligible") return false;
  if (!criterion.is_gate) {
    const gate = pathway.criteria.find((c) => c.is_gate);
    if (gate && gate.outcome !== "Passed") return false;
  }
  if (criterion.disjunction_group) {
    const groupMet = pathway.criteria.some(
      (c) =>
        c.disjunction_group === criterion.disjunction_group &&
        c.outcome === "Passed"
    );
    if (groupMet) return false;
  }
  return true;
}

/**
 * The distinct questions at a scope over some charges, in evaluation order: main criteria
 * first, then each pathway's criteria in turn. A record-scope question is carried by every
 * charge it is a question on and collected once.
 */
export function questionsAt(
  analysis: SB819AnalysisData,
  scope: SB819Scope,
  chargeIds: string[] = Object.keys(analysis.charges)
): Question[] {
  const byTarget = new Map<string, Question>();
  chargeIds.forEach((id) => {
    const charge = analysis.charges[id];
    [...charge.main_criteria, ...charge.pathways.flatMap((p) => p.criteria)]
      .filter((c) => c.scope === scope && isQuestion(c))
      .forEach((criterion) => {
        const target = answerTarget(
          criterion,
          charge.case_number,
          charge.ambiguous_charge_id
        );
        const question = byTarget.get(target) ?? {
          criterion,
          target,
          carriers: [],
        };
        question.carriers.push({ charge, criterion });
        byTarget.set(target, question);
      });
  });
  return Array.from(byTarget.values());
}

/** Answered on its target; else live if live on any charge that carries it; else dormant. */
export function stateOf(
  question: Question,
  answers: SB819Answers
): QuestionState {
  if (answers[question.target]) return "answered";
  const live = question.carriers.some(({ charge, criterion }) =>
    liveOnCharge(charge, criterion)
  );
  return live ? "live" : "dormant";
}

/** The questions a panel shows: every one that is answered or live. */
export function shown(
  questions: Question[],
  answers: SB819Answers
): Question[] {
  return questions.filter((q) => stateOf(q, answers) !== "dormant");
}

/** Whether a panel still has a live question with no answer, which holds everything below it. */
export function awaiting(
  questions: Question[],
  answers: SB819Answers
): boolean {
  return questions.some((q) => stateOf(q, answers) === "live");
}

/** The charge ids on one case, for the case's own questions. */
export function chargeIdsForCase(
  analysis: SB819AnalysisData,
  caseNumber: string
): string[] {
  return Object.values(analysis.charges)
    .filter((c) => c.case_number === caseNumber)
    .map((c) => c.ambiguous_charge_id);
}
