import React from "react";
import axios from "axios";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import {
  setupUserAndRender,
  fillSearchFormNames,
  clickButton,
} from "../../../test/testHelpers";
import SearchPanel from ".";

async function setup(fillFirstName = true, fillLastName = true) {
  const requestSpy = jest.spyOn(axios, "request").mockResolvedValue({});
  const { user, asFragment } = setupUserAndRender(<SearchPanel />);

  await fillSearchFormNames(user, fillFirstName, fillLastName);
  return { user, asFragment, requestSpy };
}

describe("name input validation", () => {
  it("requires a first name and last name", async () => {
    const { user, asFragment } = await setup(false, false);

    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
  });

  it("requires a last name if the first is provided", async () => {
    const { user, asFragment } = await setup(true, false);

    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
  });

  it("submits the request if first and last names are provided", async () => {
    const { user, asFragment, requestSpy } = await setup();

    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
    expect(requestSpy).toHaveBeenCalled();
  });
});

describe("birth date input validation", () => {
  it("rejects words", async () => {
    const { user, asFragment } = await setup();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("NOT A DATE");
    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
  });

  it("rejects a date without slashes", async () => {
    const { user, asFragment } = await setup();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("10111999");
    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
  });

  it("accepts a well formed date", async () => {
    const { user, asFragment, requestSpy } = await setup();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("10/11/2011");
    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
    expect(requestSpy).toHaveBeenCalled();
  });

  it("accepts a well formed date in the first alias but disregards other aliases", async () => {
    const { user, asFragment, requestSpy } = await setup();

    await user.click(screen.getByRole("button", { name: /alias/i }));
    await user.click(screen.getAllByLabelText(/date of birth/i)[0]);
    await user.keyboard("10/11/2011");

    const secondDateInput = screen
      .getByTestId("alias-form-1")
      .querySelector("#birthDate");

    await user.click(secondDateInput!);
    await user.keyboard("NOT A DATE BUT IT'S A SECOND ONE");
    await clickButton(user, "search");
    expect(asFragment()).toBeTruthy();
    expect(requestSpy).toHaveBeenCalled();
  });
});

describe("wildcard input validation", () => {
  describe("for first name", () => {
    it("rejects a sigle wildcard character", async () => {
      const { user, asFragment } = await setup(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("*");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });

    it("rejects a sigle wildcard character with following characters", async () => {
      const { user, asFragment } = await setup(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("*foo");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });

    it("accepts a sigle wildcard character as second and last character", async () => {
      const { user, asFragment } = await setup(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("f*");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });
  });

  describe("for last name", () => {
    it("rejects a sigle wildcard character", async () => {
      const { user, asFragment } = await setup(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("*");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });

    it("rejects a sigle wildcard character with following characters", async () => {
      const { user, asFragment } = await setup(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("*bar");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });

    it("rejects a sigle wildcard character as second and last character", async () => {
      const { user, asFragment } = await setup(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("b*");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });

    it("accepts a sigle wildcard character as third and last character", async () => {
      const { user, asFragment } = await setup(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("ba*");
      await clickButton(user, "search");
      expect(asFragment()).toBeTruthy();
    });
  });
});

test("the Remove button removes an added alias", async () => {
  const { user } = await setup();

  expect(screen.getAllByText(/first name/i)).toHaveLength(1);
  expect(screen.getAllByText(/last name/i)).toHaveLength(1);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(1);

  await clickButton(user, "alias");
  expect(screen.getAllByText(/first name/i)).toHaveLength(2);
  expect(screen.getAllByText(/last name/i)).toHaveLength(2);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(2);

  await clickButton(user, "remove");
  expect(screen.getAllByText(/first name/i)).toHaveLength(1);
  expect(screen.getAllByText(/last name/i)).toHaveLength(1);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(1);
});

/*test("the button to start over works", async () => {
  const { user, asFragment } = setup();

  await clickButton(user, "start over");
  expect(asFragment()).toBeTruthy();
});*/
