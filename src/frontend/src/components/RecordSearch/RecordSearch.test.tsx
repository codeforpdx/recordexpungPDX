import React from "react";
import { Navigate } from "react-router-dom";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import {
  appRender,
  setupUserAndRender,
  fillSearchFormNames,
} from "../../test/testHelpers";
import { useAppDispatch } from "../../redux/hooks";
import { startDemo } from "../../redux/demoSlice";
import RecordSearch from ".";

const mockHasOeciToeken = jest.fn();

jest.mock("../../service/cookie-service", () => ({
  ...jest.requireActual("../../service/cookie-service"),
  hasOeciToken: () => mockHasOeciToeken(),
}));

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  Navigate: jest.fn(),
}));

const DemoOnComponent = () => {
  useAppDispatch()(startDemo());
  return <RecordSearch />;
};

describe("when logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(true);
  });

  (["blank", "complex"] as const).forEach((fakeReponseName) => {
    it(`renders correctly with ${fakeReponseName} fake response`, () => {
      const { container } = appRender(<RecordSearch />, fakeReponseName);

      expect(container.firstChild).toMatchSnapshot();
      expect(global.window.document.title).toBe(
        "Search Records - RecordSponge"
      );
    });
  });

  it("turns off the demo state", () => {
    const { store } = appRender(<DemoOnComponent />);
    expect(store.getState().demo.isOn).toBe(false);
  });

  test("a message is displayed when the search results are empty", () => {
    appRender(<RecordSearch />, "blank");
    expect(screen.queryByText(/no search results found/i)).toBeInTheDocument();
  });

  test("a message is dislayed when results are be loaded", async () => {
    const { user } = setupUserAndRender(<RecordSearch />);

    await fillSearchFormNames(user);
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(
      screen.queryByText(/loading your search results/i)
    ).toBeInTheDocument();
  });
});

describe("when not logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(false);
  });

  it("turns off the demo state", () => {
    const { store } = appRender(<DemoOnComponent />);
    expect(store.getState().demo.isOn).toBe(false);
  });

  it("does not display content", () => {
    const { container } = appRender(<RecordSearch />, "common");
    expect(container.firstChild).toMatchSnapshot();

    expect(screen.queryByText(/date/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/search/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/case/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/assumptions/i)).not.toBeInTheDocument();
  });

  it("renders <Navigate> to /oeci", () => {
    appRender(<RecordSearch />);
    expect(Navigate).toHaveBeenCalledWith({ to: "/oeci" }, {});
  });
});
