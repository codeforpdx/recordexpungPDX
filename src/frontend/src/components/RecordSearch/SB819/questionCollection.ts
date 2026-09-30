import {
  SB819AnalysisData,
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819Scope,
  answerTarget,
} from "./types";

export interface PendingQuestion {
  criterion: SB819CriterionResultData;
  target: string;
  /** True once no charge can still be affected by the answer. */
  moot: boolean;
  /** The question upstream of this one that has not let it through, while there is one on
   * every charge. Answered against its pathway, it never will. */
  heldBy?: SB819CriterionResultData;
}

function isQuestion(criterion: SB819CriterionResultData) {
  return criterion.is_screenable && criterion.question !== null;
}

function noChargeStillAffectedBy(
  analysis: SB819AnalysisData,
  criterion: SB819CriterionResultData,
  chargeIds: string[]
) {
  return chargeIds.every((id) => {
    const charge = analysis.charges[id];
    if (charge.pathways.length === 0) return true; // a main criterion already ended it
    const pathway = charge.pathways.find(
      (p) => p.pathway === criterion.pathway
    );
    return !pathway || pathway.status === "SB-819 Ineligible";
  });
}

/**
 * The question that has to be met before this one is put to the client, if any.
 *
 * A main criterion still open on the charge comes before every pathway question, because a
 * conviction that fails it is out under every application type. Within a pathway, the gate
 * comes before the rest: it defines who the pathway is for, so a volunteer is not asked how
 * long an applicant has served before it is known that the applicant is in custody. A gate
 * that has been answered against the pathway keeps holding, since nothing behind it can
 * change anything. A question is never held by itself.
 */
export function holdingQuestion(
  charge: SB819ChargeAnalysisData,
  criterion: SB819CriterionResultData
): SB819CriterionResultData | undefined {
  if (criterion.pathway === null) return undefined;

  const openMain = charge.main_criteria.find(
    (c) => isQuestion(c) && c.outcome === "Unknown"
  );
  if (openMain) return openMain;

  if (criterion.is_gate) return undefined;
  const pathway = charge.pathways.find((p) => p.pathway === criterion.pathway);
  const gate = pathway?.criteria.find((c) => c.is_gate && isQuestion(c));
  return gate && gate.outcome !== "Passed" ? gate : undefined;
}

/**
 * The distinct questions at a given scope, in the order the criteria are evaluated.
 *
 * A record-scope question appears identically on every charge, so it is collected once.
 * Questions whose pathway is already ruled out everywhere are kept and marked moot, so the
 * reasoning stays visible without demanding an answer that changes nothing.
 * A question held back on every charge it appears on carries the question holding it; one
 * that is live on any charge is not held at all.
 */
export function collectQuestions(
  analysis: SB819AnalysisData,
  scope: SB819Scope,
  chargeIds: string[] = Object.keys(analysis.charges)
): PendingQuestion[] {
  const collected = new Map<string, PendingQuestion>();
  const holders = new Map<string, (SB819CriterionResultData | undefined)[]>();

  chargeIds.forEach((id) => {
    const charge = analysis.charges[id];
    const all = [
      ...charge.main_criteria,
      ...charge.pathways.flatMap((p) => p.criteria),
    ];
    all
      .filter((criterion) => criterion.scope === scope && isQuestion(criterion))
      .forEach((criterion) => {
        const target = answerTarget(
          criterion,
          charge.case_number,
          charge.ambiguous_charge_id
        );
        holders.set(target, [
          ...(holders.get(target) ?? []),
          holdingQuestion(charge, criterion),
        ]);
        if (collected.has(target)) return;
        collected.set(target, {
          criterion,
          target,
          moot: noChargeStillAffectedBy(analysis, criterion, chargeIds),
        });
      });
  });

  return Array.from(collected.values()).map((question) => {
    const onEachCharge = holders.get(question.target) ?? [];
    const heldEverywhere =
      onEachCharge.length > 0 && onEachCharge.every(Boolean);
    return heldEverywhere
      ? { ...question, heldBy: onEachCharge.find(Boolean) }
      : question;
  });
}

export interface PartitionedQuestions {
  /** Shown as normal: still live, or already answered. */
  asked: PendingQuestion[];
  /** Tucked away: nothing turns on them any more and nobody has answered them. */
  setAside: PendingQuestion[];
  /** The pathways whose collapse put those questions aside. */
  setAsideReason: string[];
}

/**
 * Splits questions into the ones worth showing and the ones worth folding away. A question
 * waiting on another is in neither: it appears once the question it waits on lets it
 * through.
 *
 * An answered question is never folded away, however moot it has become. It is the record
 * of a decision and the only way back from it, and hiding it would strand the volunteer
 * with an answer they could no longer change. A held question outranks a moot one: the
 * gate that holds it is the same answer that made it moot, and the volunteer never saw it,
 * so there is nothing to fold away.
 */
export function partitionQuestions(
  questions: PendingQuestion[],
  answers: { [target: string]: string | undefined }
): PartitionedQuestions {
  const answered = (q: PendingQuestion) => Boolean(answers[q.target]);
  const asked = questions.filter((q) => answered(q) || (!q.heldBy && !q.moot));
  const setAside = questions.filter((q) => !answered(q) && !q.heldBy && q.moot);
  const setAsideReason = Array.from(
    new Set(setAside.map((q) => q.criterion.pathway).filter(Boolean))
  ) as string[];
  return { asked, setAside, setAsideReason };
}

/** Charge ids belonging to one case, for gathering that case's questions. */
export function chargeIdsForCase(
  analysis: SB819AnalysisData,
  caseNumber: string
): string[] {
  return Object.values(analysis.charges)
    .filter((charge) => charge.case_number === caseNumber)
    .map((charge) => charge.ambiguous_charge_id);
}
