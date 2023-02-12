import React from "react";
import axios from "axios";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { appRender } from "../../../test/testHelpers";
import SearchPanel from ".";

function setup() {
  const user = userEvent.setup();
  const { store, asFragment } = appRender(<SearchPanel />);
  return { user, store, asFragment };
}

async function fillNames(firstName = true, lastName = true) {
  const requestSpy = jest.spyOn(axios, "request").mockResolvedValue({});

  const { user, asFragment } = setup();

  if (firstName) {
    await user.click(screen.getByLabelText(/first name/i));
    await user.keyboard("foo");
  }
  if (lastName) {
    await user.click(screen.getByLabelText(/last name/i));
    await user.keyboard("bar");
  }

  return { user, asFragment, requestSpy };
}

describe("name input validation", () => {
  it("requires a first name and last name", async () => {
    const { user, asFragment } = setup();

    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
  });

  it("requires a last name if the first is provided", async () => {
    const { user, asFragment } = setup();

    await user.click(screen.getByLabelText(/first name/i));
    await user.keyboard("foo");
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
  });

  it("submits the request if first and last names are provided", async () => {
    const { user, asFragment, requestSpy } = await fillNames();

    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
    expect(requestSpy).toHaveBeenCalled();
  });
});

describe("birth date input validation", () => {
  it("rejects words", async () => {
    const { user, asFragment } = await fillNames();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("NOT A DATE");
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
  });

  it("rejects a date without slashes", async () => {
    const { user, asFragment } = await fillNames();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("10111999");
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
  });

  it("accepts a well formed date", async () => {
    const { user, asFragment, requestSpy } = await fillNames();

    await user.click(screen.getByLabelText(/date of birth/i));
    await user.keyboard("10/11/2011");
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
    expect(requestSpy).toHaveBeenCalled();
  });

  it("accepts a well formed date in the first alias but disregards other aliases", async () => {
    const { user, asFragment, requestSpy } = await fillNames();

    await user.click(screen.getByRole("button", { name: /alias/i }));
    await user.click(screen.getAllByLabelText(/date of birth/i)[0]);
    await user.keyboard("10/11/2011");

    const secondDateInput = screen
      .getByTestId("alias-form-1")
      .querySelector("#birthDate");

    await user.click(secondDateInput!);
    await user.keyboard("NOT A DATE BUT IT'S A SECOND ONE");

    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(asFragment()).toMatchSnapshot();
    expect(requestSpy).toHaveBeenCalled();
  });
});

describe("wildcard input validation", () => {
  describe("for first name", () => {
    it("rejects a sigle wildcard character", async () => {
      const { user, asFragment } = await fillNames(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("*");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });

    it("rejects a sigle wildcard character with following characters", async () => {
      const { user, asFragment } = await fillNames(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("*foo");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });

    it("accepts a sigle wildcard character as second and last character", async () => {
      const { user, asFragment } = await fillNames(false, true);

      await user.click(screen.getByLabelText(/first name/i));
      await user.keyboard("f*");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });
  });

  describe("for last name", () => {
    it("rejects a sigle wildcard character", async () => {
      const { user, asFragment } = await fillNames(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("*");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });

    it("rejects a sigle wildcard character with following characters", async () => {
      const { user, asFragment } = await fillNames(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("*bar");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });

    it("rejects a sigle wildcard character as second and last character", async () => {
      const { user, asFragment } = await fillNames(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("b*");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });

    it("accepts a sigle wildcard character as third and last character", async () => {
      const { user, asFragment } = await fillNames(true, false);

      await user.click(screen.getByLabelText(/last name/i));
      await user.keyboard("ba*");
      await user.click(screen.getByRole("button", { name: /search/i }));

      expect(asFragment()).toMatchSnapshot();
    });
  });
});

test("the Remove button removes an added alias", async () => {
  const { user, asFragment } = await fillNames();

  expect(screen.getAllByText(/first name/i)).toHaveLength(1);
  expect(screen.getAllByText(/last name/i)).toHaveLength(1);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(1);

  await user.click(screen.getByRole("button", { name: /alias/i }));

  expect(screen.getAllByText(/first name/i)).toHaveLength(2);
  expect(screen.getAllByText(/last name/i)).toHaveLength(2);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(2);

  await user.click(screen.getAllByRole("button", { name: /remove/i })[0]);

  expect(screen.getAllByText(/first name/i)).toHaveLength(1);
  expect(screen.getAllByText(/last name/i)).toHaveLength(1);
  expect(screen.getAllByText(/date of birth/i)).toHaveLength(1);
});
