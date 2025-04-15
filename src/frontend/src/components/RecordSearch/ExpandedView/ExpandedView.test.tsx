import React from "react";
import "@testing-library/jest-dom";
import axios from "axios";
import { screen } from "@testing-library/react";
import {
  setupUserAndRender,
  clickButton,
  fillExpungementPacketForm,
} from "../../../test/testHelpers";
import ExpandedView from ".";
import { FakeResponseName } from "../../../test/hooks/useInjectSearchResponse";

function setup(recordName: FakeResponseName = "multiple", showColor = true) {
  const requestSpy = jest.spyOn(axios, "request").mockResolvedValue({});
  const { ...userAndRenderReturnValues } = setupUserAndRender(
    <ExpandedView showColor={showColor} />,
    recordName
  );
  return { requestSpy, ...userAndRenderReturnValues };
}

test("the show colors option works", () => {
  const { asFragment: asFragmentWithColor } = setup("multiple", true);
  const { asFragment: asFragmentWithoutColor } = setup("multiple", false);
  const fragmentWithColor = asFragmentWithColor();
  const fragmentWithoutColor = asFragmentWithoutColor();

  expect(fragmentWithColor).toMatchSnapshot();
  expect(fragmentWithoutColor).toMatchSnapshot();
  expect(fragmentWithColor).not.toBe(fragmentWithoutColor);
});

describe("filter checkboxes", () => {
  test("the summary checkbox that hides traffic charges works", async () => {
    const { user } = setup();

    await user.click(screen.getByTestId("hide-traffic-charges-1"));
  });

  test("the nav checkbox that hides traffic charges works", async () => {
    const { user } = setup();

    await user.click(screen.getByTestId("hide-traffic-charges-2"));
  });

  test("neither checkbox is displayed if there are no filtered cases", () => {
    setup("common");

    ["hide-traffic-charges-1", "hide-traffic-charges-2"].forEach((id) => {
      expect(screen.queryByTestId(id)).not.toBeInTheDocument();
    });
  });
});

test("the button to download the summary PDF works", async () => {
  const { user, requestSpy } = setup();

  requestSpy.mockImplementation(() => {
    return new Promise(() => {});
  });

  await clickButton(user, "summary");
  expect(requestSpy).toHaveBeenCalled();
  expect(screen.getByRole("button", { name: /download summary/i })).toHaveClass(
    "loading-btn"
  );
});

test("the button to download the expungement packet works", async () => {
  const { user, requestSpy } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await fillExpungementPacketForm(user);

  await clickButton(user, "download packet");
  expect(requestSpy).toHaveBeenCalled();
});
