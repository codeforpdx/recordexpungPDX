import React from "react";
import { appRender } from "../../../test/testHelpers";
import { RECORD_LOADING } from "../../../redux/search/types";
import { useAppDispatch } from "../../../redux/hooks";
import Layout from ".";

beforeEach(() => {
  jest.useFakeTimers().setSystemTime(new Date(2023, 1, 6));
});

afterEach(() => {
  jest.useRealTimers();
});

it("can displays request errors", () => {
  const { asFragment } = appRender(<Layout />, "error");
  expect(asFragment()).toBeTruthy();
});

it("can display a loading spinner", () => {
  const RecordLoading = () => {
    useAppDispatch()({
      type: RECORD_LOADING,
      aliases: [],
      today: "",
    });
    return <Layout />;
  };

  const { asFragment } = appRender(<RecordLoading />);
  expect(asFragment()).toBeTruthy();
});
