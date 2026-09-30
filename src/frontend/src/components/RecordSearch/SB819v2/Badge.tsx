import React from "react";
import { useAppDispatch } from "../../../redux/hooks";
import { showSB819View } from "../../../redux/sb819Slice";
import { sb819IsEnabled } from "../../../service/featureFlags";
import { SB819_HEADER_PANEL_ID, scrollToPanel } from "./panels";
import useAnalysis from "./useAnalysis";

/**
 * Sits beside the Ineligible heading in the record summary and opens the view. It reports
 * whether any analyzed conviction is still possible on the answers so far, and opens the
 * view either way, since the reasons are worth reading when nothing qualifies.
 */
export default function Badge() {
  const dispatch = useAppDispatch();
  const analysis = useAnalysis();

  if (!sb819IsEnabled() || !analysis?.has_analyzed_charges) return null;

  const possible = analysis.has_possibly_eligible;
  const label = possible
    ? "Check SB-819 eligibility"
    : "No charges SB-819 eligible";

  return (
    <button
      onClick={() => {
        dispatch(showSB819View());
        scrollToPanel(SB819_HEADER_PANEL_ID);
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
