import React from "react";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { startDemo } from "../../redux/demoSlice";
import setupPage from "../../service/setupPage";
import DemoInfo from "./DemoInfo";
import SearchPanel from "../RecordSearch/SearchPanel";
import Status from "../RecordSearch/Status";
import Record from "../RecordSearch/Record";
import Assumptions from "../RecordSearch/Assumptions";

export default function Demo() {
  const dispatch = useAppDispatch();
  let record = useAppSelector((state) => state.search.record);

  setupPage("Demo");
  dispatch(startDemo());

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
