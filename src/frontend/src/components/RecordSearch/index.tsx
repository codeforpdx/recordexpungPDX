import React from "react";
import { Redirect } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { stopDemo } from "../../redux/demoSlice";
import { hasOeciToken } from "../../service/cookie-service";
import setupPage from "../../service/setupPage";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import Assumptions from "./Assumptions";

export default function RecordSearch() {
  const record = useAppSelector((state) => state.search.record);
  const dispatch = useAppDispatch();
  let shouldRedirect = !hasOeciToken();

  setupPage("Search Records");

  dispatch(stopDemo());

  if (shouldRedirect) {
    return <Redirect to="/oeci" />;
  }

  return (
    <main className="mw8 center f6 f5-l ph2">
      <SearchPanel />
      <Status />
      <Record record={record} />
      <Assumptions />
    </main>
  );
}
