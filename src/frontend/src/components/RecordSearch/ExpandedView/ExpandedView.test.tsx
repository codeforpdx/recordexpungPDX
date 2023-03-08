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

function setup(showColor = true) {
  const requestSpy = jest.spyOn(axios, "request").mockResolvedValue({});
  const { ...userAndRenderReturnValues } = setupUserAndRender(
    <ExpandedView showColor={showColor} />,
    "multiple"
  );
  return { requestSpy, ...userAndRenderReturnValues };
}

test("the show colors option works", () => {
  const { asFragment: asFragmentWithColor } = setup(true);
  const { asFragment: asFragmentWithoutColor } = setup(false);
  const fragmentWithColor = asFragmentWithColor();
  const fragmentWithoutColor = asFragmentWithoutColor();

  expect(fragmentWithColor).toMatchSnapshot();
  expect(fragmentWithoutColor).toMatchSnapshot();
  expect(fragmentWithColor).not.toBe(fragmentWithoutColor);
});

test("the summary checkbox that hides traffic charges works", async () => {
  const { user, asFragment } = setup();

  await user.click(screen.getByTestId("hide-traffic-charges-1"));
  expect(asFragment()).toMatchSnapshot();
});

test("the nav checkbox that hides traffic charges works", async () => {
  const { user, asFragment } = setup();

  await user.click(screen.getByTestId("hide-traffic-charges-2"));
  expect(asFragment()).toMatchSnapshot();
});

test("the button to download the summary PDF works", async () => {
  const { user, requestSpy } = setup();

  await clickButton(user, "summary");
  expect(requestSpy).toHaveBeenCalled();
});

test("the button to download the expungement packet works", async () => {
  const { user, requestSpy } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await fillExpungementPacketForm(user);

  await clickButton(user, "download packet");
  expect(requestSpy).toHaveBeenCalled();
});

test("the button to start over works", async () => {
  const { user, asFragment } = setup();

  await clickButton(user, "start over");
  expect(asFragment()).toMatchSnapshot();
});
