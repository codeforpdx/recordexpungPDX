import React from "react";
import { Link } from "react-router-dom";
import { useAppDispatch } from "../../../redux/hooks";
import { hideSB819View } from "../../../redux/sb819Slice";
import scrollToPanel, {
  RECORD_SUMMARY_PANEL_ID,
  SB819_SUMMARY_PANEL_ID,
} from "./scrollToPanel";

/**
 * The top of the SB-819 view: its name, the way back to the search summary, and the rules.
 *
 * Always on screen, so the view can be left while everything below it waits on an answer.
 */
export default function SB819ViewHeader() {
  const dispatch = useAppDispatch();

  return (
    <div
      id={SB819_SUMMARY_PANEL_ID}
      className="bg-white shadow br3 mb3 ph3 pb3 scroll-mt-20"
    >
      <div className="flex flex-wrap justify-end mb1">
        <h2 className="f5 fw7 mv3 mr-auto">SB-819 Eligibility Analysis</h2>

        <button
          onClick={() => {
            dispatch(hideSB819View());
            scrollToPanel(RECORD_SUMMARY_PANEL_ID);
          }}
          className="inline-flex bg-white f6 fw5 br2 ba b--black-10 mid-gray link hover-blue pv1 ph2 mv2"
        >
          <span className="fas fa-arrow-left pr2" aria-hidden="true"></span>
          Back to Search Summary
        </button>
      </div>

      <div className="bt b--light-gray pt2">
        <Link
          to="/sb819-rules"
          className="link bb hover-blue f6 fw6"
          target="_blank"
          rel="noopener noreferrer"
        >
          Full rules
        </Link>
      </div>
    </div>
  );
}
