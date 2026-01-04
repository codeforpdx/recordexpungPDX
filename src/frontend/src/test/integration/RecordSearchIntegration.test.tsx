import React from "react";
import "@testing-library/jest-dom";
import { screen, waitFor } from "@testing-library/react";
import multipleResponse from "../data/multipleResponse";
import {
  setupIntegrationTests as setup,
  fillLoginForm,
  clickButton,
  fillSearchFormNames,
  fillExpungementPacketForm,
  fillNewCaseForm,
  goToSearchPage,
  assertRequest,
} from "../testHelpers";
import {
  expectedLoginRequest,
  expectedSearchRequest,
  expectedPacketRequest,
  expectedPdfRequest,
  expectedSecondSearchRequest,
  expectedThirdSearchRequest,
  expectedCreateCaseRequest,
  expectedUpdateCaseRequest,
  expectedRemoveCaseRequest,
  expectedAddChargeRequest,
  expectedUpdateChargeRequest,
  expectedRemoveChargeRequest,
} from "./expectedRequests/recordSearch";
import RecordSearch from "../../components/RecordSearch";
import SearchPanel from "../../components/RecordSearch/SearchPanel";

jest.setTimeout(30000);

test("Search and download summary PDF and expungement packet", async () => {
  const { user, requestSpy } = setup();

  requestSpy.mockImplementationOnce(() => {
    document.cookie = "oeci_token=1;";
    return Promise.resolve();
  });

  await goToSearchPage(user);

  // login page
  await fillLoginForm(user);
  await clickButton(user, "login");
  assertRequest(requestSpy, expectedLoginRequest);

  // wait for search form to appear after login redirect
  await waitFor(() => {
    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
  });

  // perform a search
  requestSpy.mockResolvedValue({ data: multipleResponse });
  await fillSearchFormNames(user);
  await clickButton(user, "search");
  assertRequest(requestSpy, expectedSearchRequest);
  expect(screen.queryAllByText(/baker/i)[0]).toBeInTheDocument();

  // download a summary PDF
  await clickButton(user, "summary");
  assertRequest(requestSpy, expectedPdfRequest);

  // fill out expungement packet form
  await clickButton(user, "generate paperwork");
  await fillExpungementPacketForm(user);
  await clickButton(user, "download packet");
  assertRequest(requestSpy, expectedPacketRequest);
});

// cookie still present, so still logged in
test("Submitting multiple aliases", async () => {
  const { user, requestSpy } = setup(<SearchPanel />);

  await fillSearchFormNames(user);
  await clickButton(user, "alias");

  // TODO: each Alias input fields should have unique IDs
  const secondAliasForm = screen.getByTestId("alias-form-1");
  const secondFirstNameInput = secondAliasForm.querySelector("#firstName");
  const secondLastNameInput = secondAliasForm.querySelector("#lastName");
  const secondDoBInput = secondAliasForm.querySelector("#birthDate");

  await user.click(secondFirstNameInput!);
  await user.keyboard("Rocky");
  await user.click(secondLastNameInput!);
  await user.keyboard("Balboa");
  await user.click(secondDoBInput!);
  await user.keyboard("2/23/1999");
  await clickButton(user, "search");
  assertRequest(requestSpy, expectedSecondSearchRequest);

  // remove an alias
  await clickButton(user, "remove");
  await clickButton(user, "search");
  assertRequest(requestSpy, expectedThirdSearchRequest);
});

// still logged in
test("Creating and editing a case", async () => {
  const { user, requestSpy } = setup(<RecordSearch />);

  // create a new case
  requestSpy.mockResolvedValue({ data: multipleResponse });
  await fillSearchFormNames(user);
  await clickButton(user, "enable editing");
  await clickButton(user, "add case");
  await fillNewCaseForm(user);
  await clickButton(user, "create case");
  assertRequest(requestSpy, expectedCreateCaseRequest);

  // edit a case
  await clickButton(user, "edit case");
  await user.click(screen.getByLabelText(/closed/i));
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /linn/i })
  );
  await clickButton(user, "update case");
  assertRequest(requestSpy, expectedUpdateCaseRequest);

  // remove a case
  await clickButton(user, "edit case");
  await clickButton(user, "remove case");
  assertRequest(requestSpy, expectedRemoveCaseRequest);
});

// still logged in
test("Creating and editing a charges", async () => {
  const { user, requestSpy } = setup(<RecordSearch />);

  requestSpy.mockResolvedValue({ data: multipleResponse });
  await fillSearchFormNames(user);
  await clickButton(user, "search");
  requestSpy.mockClear();

  // create a new charge
  await clickButton(user, "enable editing");
  await clickButton(user, "add charge");
  await user.click(screen.getByLabelText(/dismissed/i));
  await user.selectOptions(
    screen.getByRole("combobox", { name: /charge type/i }),
    screen.getByRole("option", { name: /fareviolation/i })
  );
  await user.selectOptions(
    screen.getByRole("combobox", { name: /severity level/i }),
    screen.getAllByRole("option", { name: /^felony class a/i })[1]
  );
  await user.click(screen.getByLabelText(/date charged/i));
  await user.keyboard("11/12/2000");
  await clickButton(user, "add charge");
  assertRequest(requestSpy, expectedAddChargeRequest);

  // edit a charge
  await clickButton(user, "edit charge");
  await user.selectOptions(
    screen.getByRole("combobox", { name: /severity level/i }),
    screen.getAllByRole("option", { name: /^misdemeanor class a/i })[1]
  );
  await user.click(screen.getByLabelText(/date charged/i));
  await user.keyboard("{Backspace>10}4/30/1777");
  await clickButton(user, "update charge");
  assertRequest(requestSpy, expectedUpdateChargeRequest);

  // remove a charge
  await clickButton(user, "edit charge");
  await clickButton(user, "remove charge");
  assertRequest(requestSpy, expectedRemoveChargeRequest);
});
