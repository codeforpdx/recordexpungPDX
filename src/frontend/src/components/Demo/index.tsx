import React, { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { startDemo } from "../../redux/search/actions";
import useSetupPage from "../../hooks/useSetupPage";
import DemoInfo from "./DemoInfo";
import SearchPanel from "../RecordSearch/SearchPanel";
import Status from "../RecordSearch/Status";
import Record from "../RecordSearch/Record";
import Assumptions from "../RecordSearch/Assumptions";
// import johnCommonRecord from "../../data/demo/johnCommon";
// import multipleCharges from "../../data/demo/multipleCharges";
// import blankRecord from "../../data/blankRecord";

export default function Demo() {
  const dispatch = useAppDispatch();
  let record = useAppSelector((state) => state.search.record);
  // record = multipleCharges;
  // record = johnCommonRecord;
  // record = blankRecord;

  useSetupPage("Demo");

  useEffect(() => {
    dispatch(startDemo());
  });

  return (
    <main className="mw8 center f6 f5-l ph2">
      <DemoInfo />
      <SearchPanel />
      <Status record={record} />
      <Record record={record} />
      <Assumptions />
    </main>
  );
}
