import React from "react";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import { CaseData } from "../Record/types";
import { awaiting, questionsAt, shown } from "./questions";
import { AnalysisData } from "./types";
import useAnalysis from "./useAnalysis";
import Header from "./Header";
import ApplicantPanel from "./ApplicantPanel";
import Summary from "./Summary";
import CasePanel from "./CasePanel";

/** The cases with a charge the analysis covers, each reduced to those charges. */
function analyzedCases(cases: CaseData[], analysis: AnalysisData): CaseData[] {
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
  const analysis = useAnalysis();

  if (!record?.cases || !analysis) return null;

  const applicant = questionsAt(analysis, "record");

  return (
    <section>
      <Header />
      <ApplicantPanel questions={shown(applicant, answers)} answers={answers} />
      {!awaiting(applicant, answers) && (
        <>
          <Summary analysis={analysis} />
          <ul className="list mb3">
            {analyzedCases(record.cases, analysis).map((aCase) => (
              <li key={aCase.case_number}>
                <CasePanel
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
