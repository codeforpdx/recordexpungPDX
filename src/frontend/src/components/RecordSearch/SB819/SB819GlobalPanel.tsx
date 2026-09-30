import React from "react";
import useSelectableDisclosure from "./useSelectableDisclosure";
import DisclosureIcon from "../../common/DisclosureIcon";
import SB819Collapse from "./SB819Collapse";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import { PartitionedQuestions } from "./questionCollection";
import SB819SetAside from "./SB819SetAside";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";

interface Props {
  questions: PartitionedQuestions;
}

/**
 * The questions that are facts about the applicant rather than about any conviction.
 *
 * Asked once here and applied to every charge, so a volunteer answers "is the applicant
 * currently incarcerated" one time instead of once per conviction. The panel opens with the
 * questions that gate a pathway and grows as they are met; it renders nothing at all while
 * every question in it waits on an answer given elsewhere.
 */
export default function SB819GlobalPanel({ questions }: Props) {
  const answers = useAppSelector(selectSB819Answers);
  const { asked, setAside, setAsideReason } = questions;
  const answered = asked.filter((q) => answers[q.target]).length;
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useSelectableDisclosure({
    id: "sb819-applicant-questions",
    isOpenToStart: true,
  });

  if (asked.length === 0 && setAside.length === 0) return null;

  return (
    <div
      id="sb819-applicant-panel"
      className="bg-white shadow br3 mb3 ph3 pb3 scroll-mt-20"
    >
      <button
        {...disclosureButtonProps}
        className="w-100 flex flex-wrap items-center bg-transparent bn pointer tl pv3 ph0"
      >
        <h3 className="f5 fw7 mr-auto">About the applicant</h3>
        <span className="f6 gray mr2">
          {asked.length > 0
            ? `${answered} of ${asked.length} answered`
            : `${setAside.length} not needed`}
        </span>
        <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
      </button>

      <SB819Collapse contentProps={disclosureContentProps}>
        <SB819QuestionBlock>
          {asked.map(({ criterion, target }) => (
            <SB819Question key={target} criterion={criterion} target={target} />
          ))}

          <SB819SetAside
            id="sb819-applicant-set-aside"
            setAside={setAside}
            setAsideReason={setAsideReason}
          />
        </SB819QuestionBlock>
      </SB819Collapse>
    </div>
  );
}
