import React from "react";
import { AnalysisData, statusColor } from "./types";

/** Every analyzed conviction under its current status, each linked to its case. */
export default function Summary({ analysis }: { analysis: AnalysisData }) {
  return (
    <div className="bg-white shadow br3 mb3 ph3 pt3 pb1">
      {analysis.sections.map(({ status, charge_ids }) => (
        <div className="mb3" key={status}>
          <div
            className={statusColor(status) + " bb b--light-gray lh-copy pb1"}
          >
            <span className="fw7">{status}</span>{" "}
            {charge_ids.length > 0 && `(${charge_ids.length})`}
          </div>
          <ul className="list">
            {charge_ids.length === 0 ? (
              <li className="f6 gray pv2">None</li>
            ) : (
              charge_ids.map((id) => {
                const charge = analysis.charges[id];
                return (
                  <li key={id} className="f6 bb b--light-gray pv2">
                    <a
                      href={"#" + charge.case_number}
                      className="link hover-blue"
                    >
                      {charge.case_number}: {charge.charge_name}
                    </a>
                  </li>
                );
              })
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}
