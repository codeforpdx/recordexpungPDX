import React from "react";
import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { appRender } from "../../test/testHelpers";
import Demo from ".";

beforeEach(() => {
  jest.useFakeTimers().setSystemTime(new Date(2023, 0, 11));
});

afterEach(() => {
  jest.useRealTimers();
});

describe("Without a record", () => {
  it("renders correctly", () => {
    const { container } = appRender(<Demo />);

    expect(container).toBeTruthy();
    expect(global.window.document.title).toBe("Demo - RecordSponge");
    expect(screen.queryByText(/search summary/i)).not.toBeInTheDocument();
  });

  it("turns on the demo state", () => {
    const { store } = appRender(<Demo />);
    expect(store.getState().demo.isOn).toBe(true);
  });
});

describe("With the multiple charges record", () => {
  it("renders correctly", () => {
    const { container } = appRender(<Demo />, "multiple");

    expect(container).toBeTruthy();
    expect(screen.queryByText(/search summary/i)).toBeInTheDocument();
  });
});
