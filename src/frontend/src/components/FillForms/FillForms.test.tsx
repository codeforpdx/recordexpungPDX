import React from "react";
import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { clickButton, setupUserAndRender } from "../../test/testHelpers";
import UserDataForm from "./UserDataForm";

const mockDownloadExpungementPacketFunc = jest.fn();

jest.mock("../../redux/search/actions", () => ({
  ...jest.requireActual("../../redux/search/actions"),
  downloadExpungementPacket: () => mockDownloadExpungementPacketFunc,
}));

function setup() {
  return setupUserAndRender(<UserDataForm />);
}

function assertModalPresentAndFormNotSubmitted() {
  expect(screen.queryByText(/incomplete/i)).toBeInTheDocument();
  expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
}

it("renders correctly on initial display", () => {
  const { asFragment } = setup();
  expect(asFragment()).toMatchSnapshot();
});

it("will not submit a blank form", async () => {
  const { user } = setup();
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("1 modal renders correctly when only name is filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("2 modal renders correctly when only name and DOB are filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("3 modal renders correctly when only name, DOB, and ZipCode are filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("4 modal renders correctly when only name, DOB, ZipCode, and PhoneNumber are filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("5 modal renders correctly when only name, DOB, ZipCode, PhoneNumber, and MailingAddress are filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await user.click(screen.getByLabelText(/address/i));
  await user.keyboard("1111 NE anywhere");
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("6 modal does NOT render when all fields are filled out", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await user.click(screen.getByLabelText(/address/i));
  await user.keyboard("1111 NE anywhere");
  await user.click(screen.getByLabelText(/city/i));
  await user.keyboard("Portland");
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /oregon/i })
  );
  await clickButton(user, "download packet");

  expect(screen.queryByText(/incomplete/i)).not.toBeInTheDocument();
  expect(mockDownloadExpungementPacketFunc).toHaveBeenCalled();
});

it("7 modal and download cannot happen at the same time when city field isnt completed", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await user.click(screen.getByLabelText(/address/i));
  await user.keyboard("1111 NE anywhere");
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /oregon/i })
  );
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});

it("8 modal and downlaod cannot happen at the same time when mailing address field isnt completed", async () => {
  const { user } = setup();

  await user.click(screen.getByLabelText(/full name/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/birth/i));
  await user.keyboard("12/12/1999");
  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");
  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await user.click(screen.getByLabelText(/city/i));
  await user.keyboard("Portland");
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /oregon/i })
  );
  await clickButton(user, "download packet");

  assertModalPresentAndFormNotSubmitted();
});
