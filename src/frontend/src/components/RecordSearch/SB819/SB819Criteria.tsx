import React, { useEffect } from "react";
import useSelectableDisclosure from "./useSelectableDisclosure";
import DisclosureIcon from "../../common/DisclosureIcon";
import SB819Collapse from "./SB819Collapse";
import { disqualifyingCriteria, resolveOutcomes } from "./resolveAnalysis";
import {
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819PathwayResultData,
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

/** The outcome, the name, and how it is settled; nothing else. */
function Criterion({ result }: { result: SB819CriterionResultData }) {
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
    </li>
  );
}

/**
 * The rows of a pathway: its screenable criteria that are not about the applicant, minus
 * the questions nothing turns on. Record-scope criteria are answered once at the top. By
 * the time the criteria are shown every live question on the charge is answered, so an
 * unknown question left here is dormant.
 */
function pathwayRows(pathway: SB819PathwayResultData) {
  return pathway.criteria.filter(
    (c) =>
      c.is_screenable &&
      c.scope !== "record" &&
      !(c.question && c.outcome === "Unknown")
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
          {pathwayRows(pathway).map((result) => (
            <Criterion key={result.key} result={result} />
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
            <Criterion key={result.key} result={result} />
          ))}
        </ul>
      </SB819Collapse>

      {analysis.pathways.map((pathway) => (
        <Pathway key={pathway.pathway} pathway={pathway} charge={analysis} />
      ))}
    </div>
  );
}
