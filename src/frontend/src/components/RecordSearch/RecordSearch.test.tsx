import React from "react";
import { MemoryRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import store from "../../redux/store";
import history from "../../service/history";
import RecordSearch from ".";

const mockHasOeciToeken = jest.fn();

jest.mock("../../redux/search/initialState", () => {
  let state = jest.requireActual("../../redux/search/initialState").default;
  state.record = jest.requireActual("../../data/demo/johnCommon").default;
  return state;
});

jest.mock("../../service/cookie-service", () => ({
  ...jest.requireActual("../../service/cookie-service"),
  hasOeciToken: () => mockHasOeciToeken(),
}));

function doRender() {
  render(
    <Provider store={store}>
      <MemoryRouter>
        <RecordSearch />
      </MemoryRouter>
    </Provider>
  );
}

describe("when logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(true);
  });

  it("renders correctly with John Common demo record", () => {
    const RealDate = global.Date;
    const mockDate = new Date(2023, 0, 11);
    // @ts-ignore
    const spy = jest.spyOn(global, "Date").mockImplementation(() => mockDate);
    // @ts-ignore
    spy.now = RealDate.now;

    const tree = renderer
      .create(
        <Provider store={store}>
          <MemoryRouter>
            <RecordSearch />
          </MemoryRouter>
        </Provider>
      )
      .toJSON();
    expect(tree).toMatchSnapshot();

    global.Date = RealDate;
  });

  it("dispatches the stop demo action", () => {
    const dispatchSpy = jest.spyOn(store, "dispatch");

    doRender();
    expect(dispatchSpy).toHaveBeenCalledWith({
      type: "STOP_DEMO",
    });
  });

  it("displays the correct document title", () => {
    doRender();
    expect(global.window.document.title).toBe("Search Records - RecordSponge");
  });

  it("does not redirect", () => {
    const historyReplaceSpy = jest.spyOn(history, "replace");

    doRender();
    expect(historyReplaceSpy).not.toHaveBeenCalled();
  });
});

describe("when not logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(false);
  });

  it("dispatches the stop demo action", () => {
    const dispatchSpy = jest.spyOn(store, "dispatch");

    doRender();
    expect(dispatchSpy).toHaveBeenCalledWith({
      type: "STOP_DEMO",
    });
  });

  it("redirects", () => {
    const historyReplaceSpy = jest.spyOn(history, "replace");

    doRender();
    expect(historyReplaceSpy).toHaveBeenCalledWith("/oeci");
  });

  it("does not display content", () => {
    doRender();
    expect(screen.queryByText(/date/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/search/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/case/i)).not.toBeInTheDocument();
  });
});
