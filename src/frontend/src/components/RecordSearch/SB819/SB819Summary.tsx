import React from "react";
import { SB819AnalysisData } from "./types";
import SB819ChargesList from "./SB819ChargesList";

interface Props {
  analysis: SB819AnalysisData;
}

/** Every analyzed conviction under its current status, each linked to its case. */
export default function SB819Summary({ analysis }: Props) {
  return (
    <div className="bg-white shadow br3 mb3 ph3 pt3 pb1">
      <SB819ChargesList analysis={analysis} />
    </div>
  );
}
