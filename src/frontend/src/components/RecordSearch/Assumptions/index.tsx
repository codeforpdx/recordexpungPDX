import React from "react";
import { HashLink as Link } from "react-router-hash-link";

export default function Assumptions() {
  return (
    <div className="bg-white shadow mb6 pa4 br3">
      <h2 className="fw6 mb3">Assumptions</h2>
      <p className="mb3">
        We are only able to access your public Oregon records.
      </p>
      <p className="mb2">
        Your analysis may be different if you have had cases:
      </p>
      <ul className="lh-copy pl4 mw6 mb3">
        <li className="mb2">Previously expunged</li>
        <li className="mb2">
          From States besides Oregon within the last ten years
        </li>
        <li className="mb2">From Federal Court within the last ten years</li>
        <li className="mb2">
          From local District Courts, e.g. Medford Municipal Court (not Jackson
          County Circuit Court) from within the last ten years
        </li>
        <li className="mb2">
          In which balances were sent to collections; due to gaps in OECI, RecordSponge may not reflect actual case balances.
        </li>
      </ul>
      <p>
        <Link className="link hover-blue underline" to="/manual#assumption1">
          Learn more in the Manual
        </Link>
      </p>
    </div>
  );
}
