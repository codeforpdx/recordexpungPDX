import React from "react";
import axios from "axios";
import { BrowserRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import store from "../../redux/store";
import multipleResponse from "../data/multipleResponse";
import {
  expectedPacketRequest,
  expectedPdfRequest,
  expectedSearchRequest,
} from "./expectedRequests/demo-search";
import App from "../../components/App";

test("Perform a demo search, download a summary PDF and download an expungement packet", async () => {
  const user = userEvent.setup();
  const requestSpy = jest
    .spyOn(axios, "request")
    .mockResolvedValue({ data: multipleResponse });

  render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  );

  // get to demo from landing page
  await user.click(screen.getAllByRole("link", { name: /search/i })[0]);
  await user.click(screen.getByRole("link", { name: /demo/i }));

  // perform a search
  await user.click(screen.getByLabelText(/first/i));
  await user.keyboard("foo");
  await user.click(screen.getByLabelText(/last/i));
  await user.keyboard("bar");
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(requestSpy).toHaveBeenCalledWith(expectedSearchRequest);

  // wait for screen to update with search results
  await waitFor(() => {
    expect(screen.queryAllByText(/baker/i)[0]).toBeInTheDocument();
  });

  // download a summary PDF
  await user.click(screen.getByRole("button", { name: /summary/i }));
  expect(requestSpy).toHaveBeenCalledWith(expectedPdfRequest);
  // mockRequest.mockClear();

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
});
