import React from "react";
import axios from "axios";
import { BrowserRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import store from "../../redux/store";
import multipleResponse from "../data/multipleResponse";
import {
  expectedLoginRequest,
  expectedSearchRequest,
  expectedPacketRequest,
  expectedPdfRequest,
  expectedSecondSearchRequest,
  expectedThirdSearchRequest,
} from "./expectedRequests/recordSearch";
import App from "../../components/App";

test("Login, perform a record search, download a summary PDF and download an expungement packet", async () => {
  const user = userEvent.setup();
  const requestSpy = jest.spyOn(axios, "request").mockImplementationOnce(() => {
    document.cookie = "oeci_token=1;";
    return Promise.resolve();
  });

  render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  );

  // landing page
  await user.click(screen.getAllByRole("link", { name: /search/i })[0]);

  // login page
  await user.click(screen.getByLabelText(/user id/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/password/i));
  await user.keyboard("secret");

  await user.click(screen.getByRole("button", { name: /log in/i }));
  expect(requestSpy).toHaveBeenCalledWith(expectedLoginRequest);

  // perform a search
  requestSpy.mockResolvedValue({ data: multipleResponse });
  requestSpy.mockClear();

  await user.click(screen.getByLabelText(/first/i));
  await user.keyboard("foo");
  await user.click(screen.getByLabelText(/last/i));
  await user.keyboard("bar");
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(requestSpy).toHaveBeenCalledWith(expectedSearchRequest);

  // screen has search results
  expect(screen.queryAllByText(/baker/i)[0]).toBeInTheDocument();

  // download a summary PDF
  await user.click(screen.getByRole("button", { name: /summary/i }));
  expect(requestSpy).toHaveBeenCalledWith(expectedPdfRequest);
  requestSpy.mockClear();

  // fill out expungement packet form
  await user.click(screen.getByRole("button", { name: /generate paperwork/i }));

  await user.click(screen.getByLabelText(/date of birth/i));
  await user.keyboard("12/12/1999");

  await user.click(screen.getByLabelText(/address/i));
  await user.keyboard("1111 NE anywhere");

  await user.click(screen.getByLabelText(/city/i));
  await user.keyboard("Portland");

  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /oregon/i })
  );

  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");

  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
  await user.click(screen.getByRole("button", { name: /download exp/i }));

  expect(requestSpy).toHaveBeenCalledWith(expectedPacketRequest);
  requestSpy.mockClear();

  // submit 2 aliases
  await user.click(screen.getAllByRole("link", { name: /search/i })[0]);
  await user.click(screen.getByRole("button", { name: /alias/i }));
  await user.click(screen.getByLabelText(/first/i));

  // add a second alias
  const secondAliasForm = screen.getByTestId("alias-form-1");
  const secondFirstNameInput = secondAliasForm.querySelector("#firstName");
  const secondLastNameInput = secondAliasForm.querySelector("#lastName");
  const secondDoBInput = secondAliasForm.querySelector("#birthDate");

  requestSpy.mockResolvedValue({ data: multipleResponse });
  await user.click(secondFirstNameInput!);
  await user.keyboard("Rocky");
  await user.click(secondLastNameInput!);
  await user.keyboard("Balboa");
  await user.click(secondDoBInput!);
  await user.keyboard("2/23/1999");
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(requestSpy).toHaveBeenCalledWith(expectedSecondSearchRequest);
  requestSpy.mockClear();

  // remove an alias
  await user.click(screen.getAllByRole("button", { name: /remove/i })[0]);
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(requestSpy).toHaveBeenCalledWith(expectedThirdSearchRequest);
  requestSpy.mockClear();
});
