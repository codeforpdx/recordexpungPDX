import React from "react";
import { BrowserRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import moment from "moment";
import store from "../../redux/store";
import App from "../../components/App";

const mockRequest = jest.fn((req) => new Promise(() => {}));

jest.mock("axios", () => {
  const recordModule = jest.requireActual("../data/multipleResponse");
  return {
    request: (request: any) => {
      mockRequest(request);
      // not sure why returning mockRequest doesn't work
      return new Promise((resolve) => {
        resolve({ data: recordModule.default });
      });
    },
  };
});

test("Perform a demo search, download a summary PDF and download an expungement packet", async () => {
  const user = userEvent.setup();
  const today = moment().format("M/D/YYYY");
  const expectedSearchRequest = {
    data: {
      aliases: [
        {
          birth_date: "",
          first_name: "foo",
          last_name: "bar",
          middle_name: "",
        },
      ],
      demo: true,
      edits: {},
      questions: {},
      today,
    },
    method: "post",
    url: "/api/demo",
    withCredentials: true,
  };
  const expectedPdfRequest = {
    data: {
      aliases: [
        {
          birth_date: "",
          first_name: "foo",
          last_name: "bar",
          middle_name: "",
        },
      ],
      demo: true,
      edits: {},
      questions: {},
      today,
    },
    method: "post",
    responseType: "blob",
    url: "/api/pdf",
    withCredentials: true,
  };
  const expectedPacketRequest = {
    data: {
      aliases: [
        {
          birth_date: "",
          first_name: "foo",
          last_name: "bar",
          middle_name: "",
        },
      ],
      demo: true,
      edits: {},
      questions: {},
      today,
      userInformation: {
        city: "Portland",
        date_of_birth: "12/12/1999",
        full_name: "foo bar",
        mailing_address: "1111 NE anywhere",
        phone_number: "123-456-7890",
        state: "Oregon",
        zip_code: "12345",
      },
    },
    method: "post",
    responseType: "blob",
    url: "/api/expungement-packet",
    withCredentials: true,
  };

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

  expect(mockRequest).toHaveBeenCalledWith(expectedSearchRequest);
  mockRequest.mockClear();

  // wait for screen to update with search results
  await waitFor(() => {
    expect(screen.queryAllByText(/baker/i)[0]).toBeInTheDocument();
  });

  // download a summary PDF
  await user.click(screen.getByRole("button", { name: /summary/i }));
  expect(mockRequest).toHaveBeenCalledWith(expectedPdfRequest);
  mockRequest.mockClear();

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

  expect(mockRequest).toHaveBeenCalledWith(expectedPacketRequest);
  mockRequest.mockClear();
});
