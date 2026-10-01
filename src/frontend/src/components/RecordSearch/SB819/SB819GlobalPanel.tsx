import React from "react";
import useSelectableDisclosure from "./useSelectableDisclosure";
import DisclosureIcon from "../../common/DisclosureIcon";
import SB819Collapse from "./SB819Collapse";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import { Question } from "./questionCollection";
import SB819Question from "./SB819Question";
import SB819QuestionBlock from "./SB819QuestionBlock";

interface Props {
  /** The record-scope questions that are answered or live. */
  questions: Question[];
}

/**
 * The questions that are facts about the applicant rather than about any conviction, asked
 * once and applied to every charge. Absent while every such question waits on a
 * main-criterion question somewhere below.
 */
export default function SB819GlobalPanel({ questions }: Props) {
  const answers = useAppSelector(selectSB819Answers);
  const answered = questions.filter((q) => answers[q.target]).length;
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useSelectableDisclosure({
    id: "sb819-applicant-questions",
    isOpenToStart: true,
  });

  if (questions.length === 0) return null;

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
          {answered} of {questions.length} answered
        </span>
        <DisclosureIcon disclosureIsExpanded={disclosureIsExpanded} />
      </button>

      <SB819Collapse contentProps={disclosureContentProps}>
        <SB819QuestionBlock>
          {questions.map(({ criterion, target }) => (
            <SB819Question key={target} criterion={criterion} target={target} />
          ))}
        </SB819QuestionBlock>
      </SB819Collapse>
    </div>
  );
}
