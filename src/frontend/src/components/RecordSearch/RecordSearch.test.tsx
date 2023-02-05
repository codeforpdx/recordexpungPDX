import React from "react";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import { appRender } from "../../test/testHelpers";
import { FakeResponseName } from "../../test/hooks/useInjectSearchResponse";
import { useAppDispatch } from "../../redux/hooks";
import { startDemo } from "../../redux/demoSlice";
import RecordSearch from ".";

const mockHasOeciToeken = jest.fn();

jest.mock("../../service/cookie-service", () => ({
  ...jest.requireActual("../../service/cookie-service"),
  hasOeciToken: () => mockHasOeciToeken(),
}));

const DemoOnComponent = () => {
  useAppDispatch()(startDemo());
  return <RecordSearch />;
};

beforeEach(() => {
  mockHasOeciToeken.mockReturnValue(true);
  jest.useFakeTimers().setSystemTime(new Date(2023, 0, 11));
});

afterEach(() => {
  jest.useRealTimers();
});

describe("when logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(true);
  });

  (["blank", "complex"] as FakeResponseName[]).forEach((fakeReponseName) => {
    it(`renders correctly with ${fakeReponseName} fake response`, () => {
      const { container } = appRender(<RecordSearch />, fakeReponseName);

      expect(container.firstChild).toMatchSnapshot();
      expect(global.window.document.title).toBe(
        "Search Records - RecordSponge"
      );
    });
  });

  it("turns off the demo state", () => {
    const { store } = appRender(<DemoOnComponent />, "common");
    expect(store.getState().demo.isOn).toBe(false);
  });
});

describe("when not logged in", () => {
  beforeEach(() => {
    mockHasOeciToeken.mockReturnValue(false);
  });

  it("turns off the demo state", () => {
    const { store } = appRender(<DemoOnComponent />, "common");
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
});
