import React from "react";
import { Redirect } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { stopDemo } from "../../redux/search/actions";
import { hasOeciToken } from "../../service/cookie-service";
import useSetupPage from "../../hooks/useSetupPage";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import Assumptions from "./Assumptions";

export default function RecordSearch() {
  const record = useAppSelector((state) => state.search.record);
  const dispatch = useAppDispatch();
  let shouldRedirect = !hasOeciToken();

  useSetupPage("Search Records");

  dispatch(stopDemo());

  if (shouldRedirect) {
    return <Redirect to="/oeci" />;
  }

  return (
    <main className="mw8 center f6 f5-l ph2">
      <SearchPanel />
      <Status record={record} />
      <Record record={record} />
      <Assumptions />
    </main>
  );
}
