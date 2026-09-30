import React from "react";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import { CaseData } from "../Record/types";
import SB819ViewHeader from "./SB819ViewHeader";
import SB819Summary from "./SB819Summary";
import SB819GlobalPanel from "./SB819GlobalPanel";
import SB819Case from "./SB819Case";
import useResolvedAnalysis from "./useResolvedAnalysis";
import { awaiting, questionsAt, shown } from "./questionCollection";
import { SB819AnalysisData } from "./types";

/** The cases with a charge the analysis covers, each reduced to those charges. */
function analyzedCases(
  cases: CaseData[],
  analysis: SB819AnalysisData
): CaseData[] {
  return cases
    .map((aCase) => ({
      ...aCase,
      charges: aCase.charges.filter(
        (c) => analysis.charges[c.ambiguous_charge_id]
      ),
    }))
    .filter((aCase) => aCase.charges.length > 0);
}

/**
 * The SB-819 view, read top down in the order the answers are needed: the header, the
 * applicant's questions, and once every live one is answered, the summary and the cases.
 */
export default function SB819View() {
  const record = useAppSelector((state) => state.search.record);
  const answers = useAppSelector(selectSB819Answers);
  const analysis = useResolvedAnalysis();

  if (!record?.cases || !analysis) return null;

  const applicant = questionsAt(analysis, "record");

  return (
    <section>
      <SB819ViewHeader />
      <SB819GlobalPanel questions={shown(applicant, answers)} />
      {!awaiting(applicant, answers) && (
        <>
          <SB819Summary analysis={analysis} />
          <ul className="list mb3">
            {analyzedCases(record.cases, analysis).map((aCase) => (
              <li key={aCase.case_number}>
                <SB819Case
                  aCase={aCase}
                  analysis={analysis}
                  answers={answers}
                />
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
