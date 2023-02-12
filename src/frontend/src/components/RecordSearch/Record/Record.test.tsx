import React from "react";
import axios from "axios";
import "@testing-library/jest-dom";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { appRender } from "../../../test/testHelpers";
import Record from ".";

// EditCasePanel accesses the store directly from the app
// and not from the Provider store in appRender so mocking the date
// is more complicated
jest.mock("../../../redux/store", () => {
  const realStoreModule = jest.requireActual("../../../redux/store");
  const initialSearchFormState = jest.requireActual(
    "../../../redux/searchFormSlice"
  ).initialState;
  const store = realStoreModule.setupStore({
    searchForm: { ...initialSearchFormState, date: "1/2/2023" },
  });

  const mockedModule = {
    __esModule: true,
    ...realStoreModule,
    default: store,
  };

  return mockedModule;
});

const expectedCreateCaseRequest = {
  data: {
    aliases: [
      { birth_date: "", first_name: "", last_name: "", middle_name: "" },
    ],
    demo: false,
    edits: {
      "CASE-0001": {
        summary: {
          balance_due: "0.01",
          birth_year: "1999",
          case_number: "CASE-0001",
          current_status: "Open",
          edit_status: "ADD",
          location: "Benton",
        },
      },
    },
    questions: undefined,
    today: "1/2/2023",
  },
  method: "post",
  url: "/api/search",
  withCredentials: true,
};

// snapshot tests for the initial state are accounted
// for in the RecordSearch tests

it("correctly renders after clicking add case button", async () => {
  const user = userEvent.setup();
  const requestSpy = jest.spyOn(axios, "request");

  const { asFragment } = appRender(<Record />);

  await user.click(screen.getByRole("button", { name: /enable editing/i }));

  // add a case
  await user.click(screen.getByRole("button", { name: /case/i }));

  // assert the form
  expect(asFragment()).toMatchSnapshot();

  await user.click(screen.getByLabelText(/open/i));
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /benton/i })
  );
  await user.click(screen.getByLabelText(/balance/i));
  // Balance already has a value of 0.00, so need to backspace first.
  await user.keyboard("{Backspace}1");
  await user.click(screen.getByLabelText(/birth year/i));
  await user.keyboard("1999");
  await user.click(screen.getByRole("button", { name: /create case/i }));

  // assert the form is closed and the Add Case button is back
  expect(asFragment()).toMatchSnapshot();

  await waitFor(() => {
    expect(requestSpy).toHaveBeenCalledWith(expectedCreateCaseRequest);
  });
});
