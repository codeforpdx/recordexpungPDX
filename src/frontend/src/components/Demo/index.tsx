import React from "react";
import { useAppDispatch } from "../../redux/hooks";
import { startDemo } from "../../redux/demoSlice";
import setupPage from "../../service/setupPage";
import DemoInfo from "./DemoInfo";
import Layout from "../RecordSearch/Layout";

export default function Demo() {
  setupPage("Demo");
  useAppDispatch()(startDemo());

  return <Layout topSection={<DemoInfo />} />;
}
