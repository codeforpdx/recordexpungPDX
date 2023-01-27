import React, { useState, useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import history from "../../service/history";
import { stopDemo } from "../../redux/search/actions";
import { hasOeciToken } from "../../service/cookie-service";
import useSetupPage from "../../hooks/useSetupPage";
import SearchPanel from "./SearchPanel";
import Record from "./Record";
import Status from "./Status";
import Assumptions from "./Assumptions";

export default function RecordSearch() {
  const [shouldDisplay, setShouldDisplay] = useState(false);
  const record = useAppSelector((state) => state.search.record);
  const dispatch = useAppDispatch();

  useSetupPage("Search Records");

  useEffect(() => {
    dispatch(stopDemo());

    if (!hasOeciToken()) {
      history.replace("/oeci");
    } else {
      setShouldDisplay(true);
    }
  }, [shouldDisplay, dispatch]);

  return shouldDisplay ? (
    <main className="mw8 center f6 f5-l ph2">
      <SearchPanel />
      <Status record={record} />
      <Record record={record} />
      <Assumptions />
    </main>
  ) : (
    <></>
  );
}
