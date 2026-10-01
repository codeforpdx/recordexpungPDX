import { useMemo } from "react";
import { useAppSelector } from "../../../redux/hooks";
import { selectSB819Answers } from "../../../redux/sb819AnswersSlice";
import resolveAnalysis from "./resolve";
import { AnalysisData } from "./types";

/** The current record's analysis with the current answers applied, or nothing to show. */
export default function useAnalysis(): AnalysisData | undefined {
  const raw = useAppSelector(
    (state) => state.search.record?.summary?.sb819_analysis
  );
  const answers = useAppSelector(selectSB819Answers);
  return useMemo(
    () => (raw ? resolveAnalysis(raw, answers) : undefined),
    [raw, answers]
  );
}
