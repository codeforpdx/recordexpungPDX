import React, { useEffect } from "react";
import useDisclosure from "../../../hooks/useDisclosure";
import DisclosureIcon from "../../common/DisclosureIcon";
import { disqualifyingCriteria, resolveOutcomes } from "./resolve";
import {
  ChargeAnalysisData,
  CriterionData,
  PathwayData,
  Status,
  statusColor,
} from "./types";

function Pill({ status }: { status: Status }) {
  const color = statusColor(status);
  return (
    <span className={`f6 fw6 br2 ph2 pv1 mr2 ${color} bg-washed-${color}`}>
      {status}
    </span>
  );
}

const OUTCOME_ICON = {
  Passed: "fas fa-check-circle green",
  Failed: "fas fa-times-circle red",
  Unknown: "fas fa-question-circle purple",
};

const DETERMINATION_STYLE: { [key: string]: string } = {
  OECI: "green bg-washed-green",
  Question: "purple bg-washed-purple",
};

/** The outcome, the name, and how it is settled; nothing else. */
function Row({ criterion }: { criterion: CriterionData }) {
  return (
    <li className="pv2 bb b--light-gray flex flex-wrap items-baseline">
      <span
        className={OUTCOME_ICON[criterion.outcome] + " mr2"}
        aria-hidden="true"
      ></span>
      <span className="fw6">{criterion.name}</span>
      <span
        className={
          "f7 fw6 br2 ph1 ml2 nowrap " +
          DETERMINATION_STYLE[criterion.determination]
        }
      >
        {criterion.determination}
      </span>
    </li>
  );
}

/**
 * Why a pathway is ruled out, as what happened: the question and the answer given, or
 * the record's own explanation. Criterion names are requirements, so a name shown as a
 * reason would state the opposite of the failure.
 */
function Bar({ criterion }: { criterion: CriterionData }) {
  if (criterion.question) {
    const answer =
      criterion.question.if_yes === "SB-819 Ineligible" ? "Yes" : "No";
    return (
      <p className="f6 mt1 mb0 ml3">
        <span className="gray">{criterion.question.text}</span>{" "}
        <span className="fw7 red">{answer}</span>
      </p>
    );
  }
  return <p className="f6 mt1 mb0 ml3 gray">{criterion.explanation}</p>;
}

interface SectionProps {
  id: string;
  heading: string;
  aside: React.ReactNode;
  openToStart: boolean;
  /** Shown under the heading while the section is closed. */
  closedNote?: React.ReactNode;
  rows: CriterionData[];
}

function Section({
  id,
  heading,
  aside,
  openToStart,
  closedNote,
  rows,
}: SectionProps) {
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
    setIsExpanded,
  } = useDisclosure({ id, isOpenToStart: openToStart });

  // An answer can settle a section after it was rendered open, and it then folds away.
  useEffect(() => {
    if (!openToStart) setIsExpanded(false);
  }, [openToStart, setIsExpanded]);

  return (
    <div className="mb3">
      <button
        {...disclosureButtonProps}
        type="button"
        className="w-100 flex flex-wrap items-center bg-transparent bn pointer tl pa0 pv2"
      >
        <h4 className="fw7 mr2">{heading}</h4>
        {aside}
        <span className="mr-auto"></span>
        <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
      </button>
      {!disclosureIsExpanded && closedNote}
      <div {...disclosureContentProps}>
        <ul className="list">
          {rows.map((c) => (
            <Row key={c.key} criterion={c} />
          ))}
        </ul>
      </div>
    </div>
  );
}

/**
 * The rows of a pathway: its screenable criteria that are not about the applicant, minus
 * the questions nothing turns on. Record-scope criteria are answered once at the top. By
 * the time the criteria are shown every live question on the charge is answered, so an
 * unknown question left here is dormant.
 */
const pathwayRows = (pathway: PathwayData) =>
  pathway.criteria.filter(
    (c) =>
      c.is_screenable &&
      c.scope !== "record" &&
      !(c.question && c.outcome === "Unknown")
  );

/** The criteria applied to one conviction and what follows from them. */
export default function Criteria({ charge }: { charge: ChargeAnalysisData }) {
  const mainStatus = resolveOutcomes(charge.main_criteria);
  const allMainPassed = mainStatus === "Possibly SB-819 Eligible";
  const id = charge.ambiguous_charge_id;

  return (
    <div className="bt b--light-gray ph3 pv3">
      <h3 className="fw7 mb2">SB-819 Limiting Criteria</h3>

      {charge.pathways.length === 0 && (
        <p className="f6 mb3">
          This conviction fails a criterion that gates every application type,
          so the Justice Integrity Unit cannot accept it under any pathway.
        </p>
      )}
      {charge.blocked_pathways.length > 0 &&
        charge.available_pathways.length > 0 && (
          <p className="f6 mb3">
            Blocked under {charge.blocked_pathways.join(", ")}, but still open
            under {charge.available_pathways.join(" and ")}.
          </p>
        )}

      <Section
        id={`sb819-main-${id}`}
        heading="Main Criteria"
        aside={
          allMainPassed ? (
            <span className="f6 green">&mdash; all four met</span>
          ) : (
            <Pill status={mainStatus} />
          )
        }
        openToStart={!allMainPassed}
        rows={charge.main_criteria}
      />

      {charge.pathways.map((pathway) => {
        const ruledOut = pathway.status === "SB-819 Ineligible";
        const bar = disqualifyingCriteria(pathway.criteria)[0];
        return (
          <Section
            key={pathway.pathway}
            id={`sb819-pathway-${id}-${pathway.pathway}`}
            heading={pathway.pathway}
            aside={<Pill status={pathway.status} />}
            openToStart={!ruledOut && pathway.pathway !== "Actual Innocence"}
            closedNote={ruledOut && bar ? <Bar criterion={bar} /> : undefined}
            rows={pathwayRows(pathway)}
          />
        );
      })}
    </div>
  );
}
