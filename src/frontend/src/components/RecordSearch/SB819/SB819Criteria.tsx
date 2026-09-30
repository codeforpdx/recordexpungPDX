import React, { useEffect } from "react";
import useSelectableDisclosure from "./useSelectableDisclosure";
import DisclosureIcon from "../../common/DisclosureIcon";
import SB819Collapse from "./SB819Collapse";
import { disqualifyingCriteria, resolveOutcomes } from "./resolveAnalysis";
import { holdingQuestion } from "./questionCollection";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import {
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819PathwayResultData,
  SB819QuestionData,
  answerTarget,
  failureReason,
  outcomeIcon,
  statusBackground,
  statusColor,
} from "./types";

function DeterminationTag({ result }: { result: SB819CriterionResultData }) {
  const styling = {
    OECI: "green bg-washed-green",
    Question: "purple bg-washed-purple",
    Discretion: "mid-gray bg-light-gray",
    "Part 2": "mid-gray bg-light-gray",
  }[result.determination];

  return (
    <span className={"f7 fw6 br2 ph1 ml2 nowrap " + styling}>
      {result.determination}
    </span>
  );
}

/** The answer a question was given, in the same shape as a pathway's stated bar. */
function AnswerLine({
  question,
  answer,
}: {
  question: SB819QuestionData;
  answer: "yes" | "no";
}) {
  const outcome = answer === "yes" ? question.if_yes : question.if_no;
  return (
    <p className="f6 mt1 mb0">
      <span className="gray">{question.text}</span>{" "}
      <span className={"fw7 " + statusColor(outcome)}>
        {answer === "yes" ? "Yes" : "No"}
      </span>
    </p>
  );
}

/**
 * Criteria whose row is the name and outcome alone. The Collateral Consequences criteria
 * and the innocence claim are each settled by a single plain question or by a document the
 * applicant assembles later, so the explanation and the answer add nothing to the icon.
 */
function isTerse(result: SB819CriterionResultData) {
  return (
    result.pathway === "Collateral Consequences" ||
    result.key === "innocence-claim"
  );
}

function Criterion({
  result,
  charge,
}: {
  result: SB819CriterionResultData;
  charge: SB819ChargeAnalysisData;
}) {
  const answers = useAppSelector(selectSB819Answers);
  // The question itself is asked in a question block above, so a criterion settled by one
  // carries only the answer it was given. A question whose gate was answered against the
  // pathway is not shown at all, since nothing turns on it and the gate's answer already
  // says so. Every other gate is answered before the reasoning is shown, so no row waits.
  const holder = result.question ? holdingQuestion(charge, result) : undefined;
  if (holder?.outcome === "Failed") return null;
  const terse = isTerse(result);

  const answer = result.question
    ? answers[
        answerTarget(result, charge.case_number, charge.ambiguous_charge_id)
      ]
    : undefined;

  return (
    <li className="pv2 bb b--light-gray">
      <div className="flex flex-wrap items-baseline">
        <span
          className={outcomeIcon(result.outcome) + " mr2"}
          aria-hidden="true"
        ></span>
        <span className="fw6">{result.name}</span>
        <DeterminationTag result={result} />
      </div>
      {!terse && <div className="f6 mt1 ml3 pl1">{result.explanation}</div>}
      {!terse && result.question && (
        <div className="ml3 pl1">
          {answer ? (
            <AnswerLine question={result.question} answer={answer} />
          ) : (
            <p className="f6 gray mt1 mb0">Not yet answered.</p>
          )}
        </div>
      )}
    </li>
  );
}

function PathwayBar({ criterion }: { criterion: SB819CriterionResultData }) {
  const reason = failureReason(criterion);

  return (
    <p className="f6 mt1 mb0 ml3">
      {reason.answer ? (
        <>
          <span className="gray">{reason.text}</span>{" "}
          <span className="fw7 red">{reason.answer}</span>
        </>
      ) : (
        <span className="gray">{reason.text}</span>
      )}
    </p>
  );
}

function Pathway({
  pathway,
  charge,
}: {
  pathway: SB819PathwayResultData;
  charge: SB819ChargeAnalysisData;
}) {
  const decided = pathway.status === "SB-819 Ineligible";
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
    setIsExpanded,
  } = useSelectableDisclosure({
    id: `pathway-${charge.ambiguous_charge_id}-${pathway.pathway}`,
    // Actual Innocence turns on a claim and an investigation, so its criteria are worth
    // reading only on request.
    isOpenToStart: !decided && pathway.pathway !== "Actual Innocence",
  });

  // An answer can rule the pathway out after it has already been rendered open, so the
  // remaining questions fold away when they stop mattering.
  useEffect(() => {
    if (decided) setIsExpanded(false);
  }, [decided, setIsExpanded]);

  // Questions about the applicant are answered once, above, so their rows are not repeated
  // on every charge. Criteria nobody can settle are not criteria rows at all.
  const own = pathway.criteria.filter(
    (c) => c.scope !== "record" && c.is_screenable
  );
  const blocker = disqualifyingCriteria(pathway.criteria)[0];

  return (
    <div className="mb3">
      <button
        {...disclosureButtonProps}
        className="w-100 flex flex-wrap items-center bg-transparent bn pointer tl pa0 pv2"
      >
        <h4 className="fw7 mr2">{pathway.pathway}</h4>
        <span
          className={`f6 fw6 br2 ph2 pv1 mr2 ${statusColor(
            pathway.status
          )} ${statusBackground(pathway.status)}`}
        >
          {pathway.status}
        </span>
        <span className="mr-auto"></span>
        <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
      </button>

      {/* Only worth saying while the questions themselves are out of sight. */}
      {decided && blocker && !disclosureIsExpanded && (
        <PathwayBar criterion={blocker} />
      )}

      <SB819Collapse contentProps={disclosureContentProps}>
        <ul className="list">
          {own.map((result) => (
            <Criterion key={result.key} result={result} charge={charge} />
          ))}
        </ul>
      </SB819Collapse>
    </div>
  );
}

interface Props {
  analysis: SB819ChargeAnalysisData;
}

/**
 * The criteria applied to one conviction and what follows from them. Rendered once every
 * question the conviction turns on has been answered, so every row is settled or moot.
 */
export default function SB819Criteria({ analysis }: Props) {
  const mainStatus = resolveOutcomes(analysis.main_criteria);
  const allMainPassed = mainStatus === "Possibly SB-819 Eligible";
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
    setIsExpanded,
  } = useSelectableDisclosure({
    id: `main-${analysis.ambiguous_charge_id}`,
    isOpenToStart: !allMainPassed,
  });

  // Answering the sentencing-level question can settle the main criteria after render.
  useEffect(() => {
    if (allMainPassed) setIsExpanded(false);
  }, [allMainPassed, setIsExpanded]);

  const blockedOnMainCriteria = analysis.pathways.length === 0;

  return (
    <div className="bt b--light-gray ph3 pv3">
      <h3 className="fw7 mb2">SB-819 Limiting Criteria</h3>

      {blockedOnMainCriteria && (
        <p className="f6 mb3">
          This conviction fails a criterion that gates every application type,
          so the Justice Integrity Unit cannot accept it under any pathway.
        </p>
      )}

      {analysis.blocked_pathways.length > 0 &&
        analysis.available_pathways.length > 0 && (
          <p className="f6 mb3">
            Blocked under {analysis.blocked_pathways.join(", ")}, but still open
            under {analysis.available_pathways.join(" and ")}.
          </p>
        )}

      <button
        {...disclosureButtonProps}
        className="w-100 flex flex-wrap items-center bg-transparent bn pointer tl pa0 pv2"
      >
        <h4 className="fw7 mr2">Main Criteria</h4>
        {allMainPassed ? (
          <span className="f6 green">&mdash; all four met</span>
        ) : (
          <span
            className={`f6 fw6 br2 ph2 pv1 mr2 ${statusColor(
              mainStatus
            )} ${statusBackground(mainStatus)}`}
          >
            {mainStatus}
          </span>
        )}
        <span className="mr-auto"></span>
        <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
      </button>
      <SB819Collapse contentProps={disclosureContentProps}>
        <ul className="list mb3">
          {analysis.main_criteria.map((result) => (
            <Criterion key={result.key} result={result} charge={analysis} />
          ))}
        </ul>
      </SB819Collapse>

      {analysis.pathways.map((pathway) => (
        <Pathway key={pathway.pathway} pathway={pathway} charge={analysis} />
      ))}
    </div>
  );
}
