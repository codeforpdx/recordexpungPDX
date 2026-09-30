import React from "react";
import { useAppDispatch } from "../../../redux/hooks";
import { showSB819View } from "../../../redux/sb819Slice";
import scrollToPanel, { SB819_SUMMARY_PANEL_ID } from "./scrollToPanel";
import { sb819IsEnabled } from "../../../service/featureFlags";
import useResolvedAnalysis from "./useResolvedAnalysis";

/** Sits beside the Ineligible heading in the search summary.
 *
 * It reports whether any ineligible Multnomah conviction survived the SB-819 limiting
 * criteria, given the answers so far, and opens the analysis either way, since the reasons
 * are worth reading even when nothing qualifies.
 */
export default function SB819Badge() {
  const dispatch = useAppDispatch();
  const analysis = useResolvedAnalysis();

  if (!sb819IsEnabled()) return null;
  if (!analysis?.has_analyzed_charges) return null;

  const possible = analysis.has_possibly_eligible;
  const label = possible
    ? "Check SB-819 eligibility"
    : "No charges SB-819 eligible";

  return (
    <button
      onClick={() => {
        dispatch(showSB819View());
        scrollToPanel(SB819_SUMMARY_PANEL_ID);
      }}
      aria-label={`${label}. Open the SB-819 eligibility analysis.`}
      className={
        "inline-flex items-center f6 fw6 br3 ba pv1 ph2 ml2 pointer hover-bg-white " +
        (possible
          ? "purple bg-washed-purple b--light-purple"
          : "red bg-washed-red b--light-red")
      }
    >
      <span className="fas fa-scale-balanced pr2" aria-hidden="true"></span>
      {label}
      <span className="fas fa-chevron-right pl2 f7" aria-hidden="true"></span>
    </button>
  );
}
