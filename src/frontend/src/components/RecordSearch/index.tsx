import React from "react";
import { Redirect } from "react-router-dom";
import { useAppDispatch } from "../../redux/hooks";
import { stopDemo } from "../../redux/demoSlice";
import { hasOeciToken } from "../../service/cookie-service";
import setupPage from "../../service/setupPage";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import Assumptions from "./Assumptions";

export default function RecordSearch() {
  setupPage("Search Records");
  useAppDispatch()(stopDemo());

  if (!hasOeciToken()) {
    return <Redirect to="/oeci" />;
  }

  return (
    <main className="mw8 center f6 f5-l ph2">
      <SearchPanel />
      <Status />
      <Record />
      <Assumptions />
    </main>
  );
}
