import React from "react";
import { MemoryRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { Provider } from "react-redux";
import store from "../../redux/store";
import Demo from ".";

const mockUseAppSelector = jest.fn();

jest.mock("../../redux/hooks", () => ({
  ...jest.requireActual("../../redux/hooks"),
  useAppSelector: () => mockUseAppSelector(),
}));

function doRender() {
  render(
    <Provider store={store}>
      <MemoryRouter>
        <Demo />
      </MemoryRouter>
    </Provider>
  );
}

it("renders correctly without a record", () => {
  const RealDate = Date;
  const mockDate = new Date(2023, 0, 11);
  // @ts-ignore
  const spy = jest.spyOn(global, "Date").mockImplementation(() => mockDate);
  // @ts-ignore
  spy.now = RealDate.now;

  const tree = renderer
    .create(
      <Provider store={store}>
        <MemoryRouter>
          <Demo />
        </MemoryRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();

  global.Date = RealDate;
});

describe("Without a record", () => {
  it("calls useAppSelector", () => {
    doRender();
    expect(mockUseAppSelector).toHaveBeenCalled();
  });

  it("dispatches the stop demo action", () => {
    const dispatchSpy = jest.spyOn(store, "dispatch");

    doRender();
    expect(dispatchSpy).toHaveBeenCalledWith({
      type: "START_DEMO",
    });
  });

  it("displays the correct document title", () => {
    doRender();
    expect(global.window.document.title).toBe("Demo - RecordSponge");
  });

  it("does not display search summary", () => {
    expect(screen.queryByText(/search summary/i)).not.toBeInTheDocument();
  });
});
