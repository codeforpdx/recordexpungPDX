import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import {
  setupIntegrationTests,
  clickButton,
  fillSearchFormNames,
  fillExpungementPacketForm,
  goToSearchPage,
  assertRequest,
} from "../testHelpers";
import multipleResponse from "../data/multipleResponse";
import {
  expectedPdfRequest,
  expectedPacketRequest,
} from "./expectedRequests/recordSearch";

beforeAll(() => {
  document.cookie = "oeci_token=1;";
});

test("Download summary PDF and expungement packet", async () => {
  const { user, requestSpy } = setupIntegrationTests();

  requestSpy.mockResolvedValue({ data: multipleResponse });
  await goToSearchPage(user);
  await fillSearchFormNames(user);
  await clickButton(user, "search");
  await user.click(screen.getByRole("radio", { name: /expanded/i }));
  await clickButton(user, "summary");
  assertRequest(requestSpy, expectedPdfRequest);

  await fillExpungementPacketForm(user, 1);
  await clickButton(user, "download packet");
  assertRequest(requestSpy, expectedPacketRequest);
});
